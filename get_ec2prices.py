import boto3
import json
import pprint

region_mapping_dict = {'us-east-2': 'US East (Ohio)',
                            'us-east-1': 'US East (N. Virginia)',
                            'us-west-1': 'US West (N. California)',
                            'us-west-2': 'US West (Oregon)',
                            'ap-south-1': 'Asia Pacific (Mumbai)',
                            'ap-northeast-2': 'Asia Pacific (Seoul)',
                            'ap-southeast-1': 'Asia Pacific (Singapore)',
                            'ap-southeast-2': 'Asia Pacific (Sydney)',
                            'ap-northeast-1': 'Asia Pacific (Tokyo)',
                            'ca-central-1': 'Canada (Central)',
                            'cn-north-1': 'China (Beijing)',
                            'cn-northwest-1': 'China (Ningxia)',
                            'eu-central-1': 'EU (Frankfurt)',
                            'eu-west-1': 'EU (Ireland)',
                            'eu-west-2': 'EU (London)',
                            'eu-west-3': 'EU (Paris)',
                            'eu-north-1': 'EU (Stockholm)',
                            'sa-east-1': 'South America (Sao Paulo)'}

pricing = boto3.client('pricing')

def get_instance_prices(instance_name, region):
		queryfilter = [ 
				{'Type' :'TERM_MATCH', 'Field':'location',		'Value':region_mapping_dict[region]},
				{'Type' :'TERM_MATCH', 'Field':'operatingSystem', 'Value':'Linux'			},
				{'Type' :'TERM_MATCH', 'Field':'preInstalledSw',  'Value':'NA'	},
				{'Type' :'TERM_MATCH', 'Field':'productFamily',   'Value':'Compute Instance'	},
				{'Type' :'TERM_MATCH', 'Field':'tenancy',		 'Value':'Shared'			  },
				{'Type' :'TERM_MATCH', 'Field':'instanceType',	'Value':instance_name		 },
				{'Type' :'TERM_MATCH', 'Field':'capacitystatus',  'Value':'Used'				},
		]
		response = pricing.get_products(ServiceCode='AmazonEC2',Filters=queryfilter,MaxResults=100)
		details={}
		details['price'] = {}

		for price in response['PriceList']:
				xprice = json.loads(price)
				details['instance'] = xprice["product"]["attributes"]["instanceType"]
				details['region'] = region
				details['memory'] = xprice["product"]["attributes"]["memory"]
				details['vcpu'] = xprice["product"]["attributes"]["vcpu"]
				details['family'] = xprice["product"]["attributes"]["instanceFamily"]
				if 'physicalProcessor' in price : details['processor'] = xprice["product"]["attributes"]["physicalProcessor"]
				if 'clockSpeed' in price : details['clock'] = xprice["product"]["attributes"]["clockSpeed"] 
				if 'networkPerformance' in price : details['network'] = xprice["product"]["attributes"]["networkPerformance"]
				if 'currentGeneration' in price : details['current'] = xprice["product"]["attributes"]["currentGeneration"]
				if 'dedicatedEbsThroughput' in price : details['ebsperf'] = xprice["product"]["attributes"]["dedicatedEbsThroughput"]
				if 'storage' in price : details['storage'] = xprice["product"]["attributes"]["storage"]
				details['os'] = xprice["product"]["attributes"]["operatingSystem"]
				details['sw'] = xprice["product"]["attributes"]["preInstalledSw"]
				for item in xprice["terms"]:
						
						od = item
						
						for id1 in list(xprice["terms"][od]):
							if od == 'Reserved':
								RIperiod = xprice["terms"][od][id1]['termAttributes']['LeaseContractLength']
								RItype = xprice["terms"][od][id1]['termAttributes']['OfferingClass']
								RIpay = xprice["terms"][od][id1]['termAttributes']['PurchaseOption']
								if od not in details['price']: 
									details['price'][od] = {}
								if RIperiod not in details['price'][od]:
									details['price'][od][RIperiod] = {}
								if RItype not in details['price'][od][RIperiod]:
									details['price'][od][RIperiod][RItype]={}
								if RIpay not in details['price'][od][RIperiod][RItype]: 
									details['price'][od][RIperiod][RItype][RIpay] = []
							else: 
								details['price'][od] = {}
							
							
							for id2 in  list(xprice["terms"][od][id1]['priceDimensions']):
								miniprice = {}
								miniprice['unitprice'] =  xprice["terms"][od][id1]['priceDimensions'][id2]['pricePerUnit']['USD']
								miniprice['unit'] =  xprice["terms"][od][id1]['priceDimensions'][id2]['unit']
								miniprice['descr'] =  xprice["terms"][od][id1]['priceDimensions'][id2]['description']
							
								if od == 'Reserved':
									details['price'][od][RIperiod][RItype][RIpay].append(miniprice)
								else: 
									details['price'][od] = miniprice

						
		return details

        
def get_instances(Token, values):
        response = pricing.get_attribute_values(ServiceCode='AmazonEC2', AttributeName="instanceType", NextToken=Token,MaxResults=100)
        for instance in response["AttributeValues"]:
                values.append(instance["Value"])

        if 'NextToken' in response:
                NT = response["NextToken"]
                get_instances(response["NextToken"], values)
        return values
        

instances = []
get_instances("", instances)

prices = {}
prices['Items'] = []
for item in instances:
        if "." in item: 
                response = get_instance_prices(item, 'us-east-1')
                prices['Items'].append(response)
print (json.dumps(prices))
