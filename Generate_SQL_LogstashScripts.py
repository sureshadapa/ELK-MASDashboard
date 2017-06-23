import ConfigParser,sys,subprocess,os

Config = ConfigParser.ConfigParser()
print Config.read("./Configuration.ini")
#print Config.sections()

def CheckEnvironment():
    try:
        retcode = subprocess.call("rpm -qa | grep '^python-2.'", shell=True)
        if retcode == 0:
            print >>sys.stderr, "Python is installed on this Linux VM/System.", -retcode
        else:
            print >>sys.stderr, "Python NOT found on this Linux VM/System.Please contact Administrator.", retcode
            sys.exit()
    except OSError as e:
        print >>sys.stderr, "Execution failed:", e
        sys.exit()

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def GenerateMAConfig(marketarea):
    file = open(marketarea+".cfg", "w")
    file.write("# Python script generated logstash configuration script for MarketArea "+marketarea+".\n");
    file.write("input {\n");
    file.write("    jdbc {\n");
    file.write("        # Postgres jdbc connection string to our database, mydb\n");
    file.write("        jdbc_connection_string => \""+ConfigSectionMap("Application-Settings")['jdbc_connection_string']+"\"\n");
    file.write("        # The user we wish to execute our statement as\n");
    file.write("        jdbc_user => \""+ConfigSectionMap("Application-Settings")['jdbc_user']+"\"\n");
    file.write("        jdbc_password => \""+ConfigSectionMap("Application-Settings")['jdbc_password']+"\"\n");
    file.write("        # The path to our downloaded jdbc driver\n");
    file.write("        jdbc_driver_library => \""+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/"+ConfigSectionMap("Application-Settings")['jdbc_driver_library']+"\"\n");
    file.write("        # The name of the driver class for Postgresql\n");
    file.write("        jdbc_driver_class => \""+ConfigSectionMap("Application-Settings")['jdbc_driver_class']+"\"\n");
    file.write("        # our query\n");
    file.write("        statement_filepath => \""+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/"+marketarea+".sql\"\n");
    file.write("    }\n");
    file.write("}\n");
    
    file.write("output {\n");
    file.write("    elasticsearch {\n");
    file.write("        protocol => http\n");
    file.write("        index => \""+marketarea.lower()+"_car\"\n");
    file.write("        document_type => \""+marketarea.lower()+"_car_doc\"\n");
    file.write("        host => \""+ConfigSectionMap("Application-Settings")['elasticsearch_host']+"\"\n");
    file.write("        port => \""+ConfigSectionMap("Application-Settings")['elasticsearch_port']+"\"\n");
    file.write("    }\n");
    file.write("}\n");
    file.close()

def GenerateCustomerInfoConfig():
    file = open("MAS_Customer_Info.cfg", "w")
    file.write("# Python script generated logstash configuration script for fetching Customer Information.\n");
    file.write("input {\n");
    file.write("    jdbc {\n");
    file.write("        # Postgres jdbc connection string to our database, mydb\n");
    file.write("        jdbc_connection_string => \""+ConfigSectionMap("Application-Settings")['jdbc_connection_string']+"\"\n");
    file.write("        # The user we wish to execute our statement as\n");
    file.write("        jdbc_user => \""+ConfigSectionMap("Application-Settings")['jdbc_user']+"\"\n");
    file.write("        jdbc_password => \""+ConfigSectionMap("Application-Settings")['jdbc_password']+"\"\n");
    file.write("        # The path to our downloaded jdbc driver\n");
    file.write("        jdbc_driver_library => \""+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/"+ConfigSectionMap("Application-Settings")['jdbc_driver_library']+"\"\n");
    file.write("        # The name of the driver class for Postgresql\n");
    file.write("        jdbc_driver_class => \""+ConfigSectionMap("Application-Settings")['jdbc_driver_class']+"\"\n");
    file.write("        # our query\n");
    file.write("        statement_filepath => \""+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/"+ConfigSectionMap("Application-Settings")['jdbc_sql4_customerinfo']+"\"\n");
    file.write("    }\n");
    file.write("}\n");

    file.write("output {\n");
    file.write("    elasticsearch {\n");
    file.write("        protocol => http\n");
    file.write("        index => \"customers_at_risk_v3\"\n");
    file.write("        document_type => \"customers_risk_doc_v3\"\n");
    file.write("        document_id => \"%{customer_unique_id}\"\n");
    file.write("        host => \""+ConfigSectionMap("Application-Settings")['elasticsearch_host']+"\"\n");
    file.write("        port => \""+ConfigSectionMap("Application-Settings")['elasticsearch_port']+"\"\n");
    file.write("        retry_max_interval => 6\n");
    file.write("        max_retries => 1\n");
    file.write("    }\n");
    file.write("}\n");
    file.close()



def GenerateMALibsConfig():
    str_file = ConfigSectionMap("Application-Settings")['logstash_configpath']+"/"+ConfigSectionMap("Application-Settings")['logstash_cfg4_manlibs']
    file = open(str_file, "w")
    file.write("# Python script generated logstash configuration script for fetching MarketArea and corresponding libraries.\n");
    file.write("input {\n");
    file.write("    jdbc {\n");
    file.write("        # Postgres jdbc connection string to our database, mydb\n");
    file.write("        jdbc_connection_string => \""+ConfigSectionMap("Application-Settings")['jdbc_connection_string']+"\"\n");
    file.write("        # The user we wish to execute our statement as\n");
    file.write("        jdbc_user => \""+ConfigSectionMap("Application-Settings")['jdbc_user']+"\"\n");
    file.write("        jdbc_password => \""+ConfigSectionMap("Application-Settings")['jdbc_password']+"\"\n");
    file.write("        # The path to our downloaded jdbc driver\n");
    file.write("        jdbc_driver_library => \""+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/"+ConfigSectionMap("Application-Settings")['jdbc_driver_library']+"\"\n");
    file.write("        # The name of the driver class for Postgresql\n");
    file.write("        jdbc_driver_class => \""+ConfigSectionMap("Application-Settings")['jdbc_driver_class']+"\"\n");
    file.write("        # our query\n");
    file.write("        statement_filepath => \""+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/"+ConfigSectionMap("Application-Settings")['jdbc_sql4_manlibs']+"\"\n");
    file.write("    }\n");
    file.write("}\n");

    file.write("output {\n");
    file.write("  file {");
    file.write("         path => \""+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/"+ConfigSectionMap("Application-Settings")['manlibs_outputfile']+"\"\n");
    file.write("  }");
    file.write("}\n");
    file.close()
    


def RunMACfg():
    str_command = ConfigSectionMap("Application-Settings")['logstash_basepath']+"/bin/logstash  -f  "+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/"+ConfigSectionMap("Application-Settings")['logstash_cfg4_manlibs']
    try:
        retcode = subprocess.call(str_command, shell=True)
        if retcode == 0:
            print >>sys.stderr, "MarketArea and Libraries information fetched.", -retcode
        else:
            print >>sys.stderr, "MarketArea and Libraries information NOT fetched..Please contact Administrator.", retcode
            sys.exit()
    except OSError as e:
        print >>sys.stderr, "Execution failed:", e
        sys.exit()


def GenerateCronSH(marketarea):
   file = open(ConfigSectionMap("Application-Settings")['logstash_configpath']+"/"+marketarea+"_cron.sh", "w")
   file.write("#!/bin/bash\n\n");
   file.write("curl -XDELETE 'http://"+ConfigSectionMap("Application-Settings")['elasticsearch_host']+":"+ConfigSectionMap("Application-Settings")['elasticsearch_port']+"/"+marketarea.lower()+"_car/' | grep '\"acknowledged\":true'\n");
   file.write("if [ $? -eq 0 ]\n");
   file.write("then\n");
   file.write("  echo \"Successfully deleted existing index file\"\n");
   file.write("  echo \"Recreating index file for "+marketarea+" on `date` \"\n");
   #file.write( ConfigSectionMap("Application-Settings")['logstash_basepath']+"/bin/logstash -f "+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/"+marketarea+".cfg  --log "+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/cronjob.log\n");
   file.write( ConfigSectionMap("Application-Settings")['logstash_basepath']+"/bin/logstash -f "+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/"+marketarea+".cfg\n");
   file.write("else\n");
   file.write("  echo \"Creating new index file for "+marketarea+" on `date` \"\n");
   #file.write( ConfigSectionMap("Application-Settings")['logstash_basepath']+"/bin/logstash -f "+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/"+marketarea+".cfg  --log "+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/cronjob.log\n");
   file.write( ConfigSectionMap("Application-Settings")['logstash_basepath']+"/bin/logstash -f "+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/"+marketarea+".cfg\n");
   file.write("fi\n");
   file.close()

def GenerateCustomerCronSH():
   file = open(ConfigSectionMap("Application-Settings")['logstash_configpath']+"/MAS_CUST_cron.sh", "w")
   file.write("#!/bin/bash\n\n");
   file.write("curl -XDELETE 'http://"+ConfigSectionMap("Application-Settings")['elasticsearch_host']+":"+ConfigSectionMap("Application-Settings")['elasticsearch_port']+"/customers_at_risk_v3' | grep '\"acknowledged\":true'\n");
   file.write("if [ $? -eq 0 ]\n");
   file.write("then\n");
   file.write("  echo \"Successfully deleted existing index file\"\n");
   file.write("  echo \"Recreating index file for customers_at_risk_v3 on `date` \"\n");
   file.write( ConfigSectionMap("Application-Settings")['logstash_basepath']+"/bin/logstash -f "+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/MAS_Customer_Info.cfg\n");
   file.write("else\n");
   file.write("  echo \"Creating new index file for customers_at_risk_v3 on `date` \"\n");
   file.write( ConfigSectionMap("Application-Settings")['logstash_basepath']+"/bin/logstash -f "+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/MAS_Customer_Info.cfg\n");
   file.write("fi\n");
   file.close()
  

# Check the OS environment to check if python exists or not.
CheckEnvironment()

# Generate Customer Information related logstash configuration file.
print "Generating customer information logstash configuration file."
GenerateCustomerInfoConfig()

# Generate logstash configuration file for the marketares and their corresponding libraries information.
print "Generate MarketArea Vs MAS Libraries information logstash configuration file."
GenerateMALibsConfig()


# Run logstash to fetch marketares and their corresponding libraries information into flatfile.
print "Pulling MarketArea Vs MAS Libraries information MAS DB2 into flatfile."
RunMACfg()

# read the above flatfile and generate dynamic sql files,logstash configuration files and associated cronjob shell script for each Marketarea.
print "Generating Dynamic SQL files, Logstash Configuration files and Associated Cronjob Shell Script files for each MarketArea."
ff = open(ConfigSectionMap("Application-Settings")['logstash_configpath']+"/"+ConfigSectionMap("Application-Settings")['manlibs_outputfile'],"r")
lines = ff.readlines()
TMP_MA=''
i = 0
for ll in lines:
	MA = ll.strip("\n").split(",")[0].split(":")[1].replace('"','')
	LIB = ll.strip("\n").split(",")[1].split(":")[1].replace('"','')
	if TMP_MA != MA:
		if i !=0:
			fw = open(ConfigSectionMap("Application-Settings")['logstash_configpath']+"/"+TMP_MA+".sql","w")
			#print TMP_MA+"::"+ FINAL_SQL
			fw.write(FINAL_SQL)
			fw.close()
                        GenerateMAConfig(TMP_MA)
                        GenerateCronSH(TMP_MA)
		SQL="WITH REVENUE AS ( SELECT W.CSTUNIQ# AS CUSTOMER_UNIQUE_ID, sum(SVCHRG) AS SUM_SVCHRG FROM \""+LIB+"\".AR#TXHST T LEFT OUTER join MASLIBRS.W1000 W ON T.COMPNY = W.COMPNY AND T.CUSTOMER# = W.CUSTOMER# WHERE W.LIBRARY = '"+LIB+"'  AND W.BUSINESS_UNIT <> 0 AND T.RECTYP ='S' and MANBIL <> 'Y' AND T.PERIOD >=  DEC(SUBSTR( replace(char(current date - 12 MONTHS ,ISO),'-',''),1,6)) AND T.PERIOD <=DEC(SUBSTR( replace(char(current date- 1 MONTHS, ISO),'-',''),1,6)) GROUP BY W.CSTUNIQ#"
	if TMP_MA == MA:
		SQL= SQL+" UNION ALL "+" SELECT W.CSTUNIQ# AS CUSTOMER_UNIQUE_ID, sum(SVCHRG) AS SUM_SVCHRG FROM \""+LIB+"\".AR#TXHST T LEFT OUTER join MASLIBRS.W1000 W ON T.COMPNY = W.COMPNY AND T.CUSTOMER# = W.CUSTOMER# WHERE W.LIBRARY = '"+LIB+"'  AND W.BUSINESS_UNIT <> 0 AND T.RECTYP ='S' and MANBIL <> 'Y' AND T.PERIOD >=  DEC(SUBSTR( replace(char(current date - 12 MONTHS ,ISO),'-',''),1,6)) AND T.PERIOD <=DEC(SUBSTR( replace(char(current date- 1 MONTHS, ISO),'-',''),1,6)) GROUP BY W.CSTUNIQ#"
	TMP_MA=MA
	i=i+1
	FINAL_SQL = SQL + ") SELECT TRIM(A1.CSTUNIQ#) AS CUSTOMER_UNIQUE_ID, REPLACE(SUBSTR(B1.FOCUSTIER,3),' ','') AS \"Focus_Tier\",TRIM(A1.COMPANY) AS \"Company_Code\", TRIM(A1.CUSTOMER_NUMBER) AS \"Customer_Number\",TRIM(A1.NAME) AS \"Name\", TRIM(A1.PHONE_NUMBER) AS \"Contact_Phone\", A1.FAX_NUMBER,TRIM(A1.HOUSE_NUMBER)||','||TRIM(A1.STREET)||','||TRIM(A1.CITY)||','||TRIM(A1.STATE)||','||TRIM(A1.ZIP_CODE) AS \"Service_Address\" , TRIM(C1.FACWMSIDU) AS MSA_IDU,TRIM(C1.FACMAIDU) AS MARKET_AREA,TRIM(C1.FACMANAME) AS MARKET_AREA_DESCRIPTION,TRIM(REPLACE(REPLACE(C1.FACNAME,' ',''),'-','')) AS BU, TRIM(C1.FACGRPNAME) AS GROUP_NAME_ID,TRIM(C1.FACMASSUBI) AS MARKET_AREA_SUBID, TRIM(C1.FACMASSUBN) AS MARKET_AREA_SUBNAME,TRIM(C1.FACWMSIDU) AS MSA_IDU,  R.SUM_SVCHRG,  TRIM(A1.BUSINESS_UNIT) AS BUNIT,DEC(SUBSTR( replace(char(current date - 12 MONTHS ,ISO),'-',''),1,6)) FromPeriod,DEC(SUBSTR( replace(char(current date- 1 MONTHS, ISO),'-',''),1,6)) ToPeriod FROM MASLIBRS.W1000 A1 JOIN MASLIBRS.FOCUSTRPF B1 ON A1.CSTUNIQ#= B1.CSTUNIQ# JOIN REVENUE R ON B1.CSTUNIQ# = R.CUSTOMER_UNIQUE_ID AND A1.BUSINESS_UNIT <> 0 JOIN MASLIBRS.SC#CORPDB C1 ON A1.BUSINESS_UNIT = C1.MASBU AND C1.FACMAIDU= '"+TMP_MA+"'"
#print TMP_MA+"::"+FINAL_SQL
fw = open(ConfigSectionMap("Application-Settings")['logstash_configpath']+"/"+TMP_MA+".sql","w")
fw.write(FINAL_SQL)
fw.close()
GenerateMAConfig(TMP_MA)
GenerateCronSH(TMP_MA)
GenerateCustomerCronSH()

cmd="chmod 744 "+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/*.sql  "+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/*.sh  "+ConfigSectionMap("Application-Settings")['logstash_configpath']+"/*.cfg"
os.system(cmd)
