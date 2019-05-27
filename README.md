# AWS EC2 Prices
Getting the most current pricing options (and there are many options for each instance) is always a challenge. 

The idea behind this script is to provide a simple way to gather pricing data using the most current <a href="https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing.html/"> BOTO3 Pricing API </a> and simplify the output with the relevant fields. 

The output JSON follows the following format: 

      {  
         "instance":"a1.2xlarge",
         "memory":"16 GiB",
         "vcpu":"8",
         "family":"General purpose"
         "price":[  
            {  
               "os":"Linux",
               "sw":"NA",
               "mode":"OnDemand",
               "unit":"Hrs",
               "unitprice":"0.2040000000",
               "unitpricedesc":"$0.204 per On Demand Linux a1.2xlarge Instance Hour",
               "terms":{  

               }
            },
            {  
               "os":"SUSE",
               "sw":"NA",
               "mode":"Reserved",
               "unit":"Hrs",
               "unitprice":"0.1553000000",
               "unitpricedesc":"SUSE Linux (Amazon VPC), a1.2xlarge reserved instance applied",
               "terms":{  
                  "LeaseContractLength":"3yr",
                  "OfferingClass":"convertible",
                  "PurchaseOption":"No Upfront"
               }
            },
            ...
         ]
      }
`
