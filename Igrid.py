import dns.resolver
import whois
import os
import json
import requests


data_dictionary = {}
def main():
    filename = "Igrid.txt" # A text file containing a list of domains 
    path =  os.getcwd()
    print("This is the IGRID Assesment\n")
    print("Current Working Directory is :: " , path ) # Prints the current working directory
    print("The input file containing containing a list of domains is :: " , filename) 
    
    try:
        f= open(filename, "r")
       # for line in f:
        while True:
            line = f.readline()
            if not line:
                break
            domain_name = line.strip()
            lighthouse_performance_score(domain_name) 
            parse_dns_records(domain_name)
            registrar_details(domain_name)

        f.close()
    except IOError:
       print("File not found!!!")
    finally:
             write_to_json(data_dictionary)


def lighthouse_performance_score(url):
    lighthouse_url='https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url='
    parameters = '&category=PERFORMANCE&strategy=STRATEGY_UNSPECIFIED&prettyPrint=true&alt=json'
    website = 'http://www.'+ url
    uri = lighthouse_url+website+ parameters
    performance = requests.get(uri)
    result = performance.json()
    print(uri)
    data_dictionary.update(result)
    print(result)
    
def parse_dns_records(domain_name):
    print('\n The domain name is ::=> '+ domain_name)
 
    dns_type = ['NONE','A','NS','CNAME','SOA','MX','AAAA',
   'CSYNC','TXT','CAA']
    
    for a in dns_type:
        try:
            answers = dns.resolver.query(domain_name, a)
            for rdata in answers: 
                y = {a : rdata.to_text()}
                print(y)
                data_dictionary.update(y)

              
    
        except Exception as e:
            print(e)  # or pass

def registrar_details(domain_name):
   try:
       w = whois.whois(domain_name)

       whois_info = whois.whois(domain_name)
       print("DOMAIN REGISTRAR: ",whois_info.registrar)
       print("WHOIS SERVER: ", whois_info.whois_server)
       print("Domain Creation Date: ",whois_info.creation_date)
       print("Expiration Date: ", whois_info.expiration_date)
       print(whois_info)
         
       
       d ={"DOMAIN REGISTRAR: ",whois_info.registrar,
                    "WHOIS SERVER: ", whois_info.whois_server,
                    "Domain Creation Date: ",whois_info.creation_date,
                    "Expiration Date: ", whois_info.expiration_date
                    }
       data_dictionary.update(d)

       print("\n")

   except Exception:
        return False
   else:
        return bool(w.domain_name)   


def write_to_json(json_message):
    json_object = json.dumps(json_message, indent = 4)
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)


if __name__ == '__main__':
    main()



