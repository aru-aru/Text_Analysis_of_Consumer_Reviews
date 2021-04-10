
import os
import pandas as pd

project_dir = r'D:\GitHub\Projects\Analysis_of_Delivery_Companies_Reviews'
os.chdir(project_dir)

import trustplt as pilot

source_url = 'https://uk.trustpilot.com'
company_url = '/review/www.deliveroo.co.uk'
landing_page = source_url + company_url

processed_pages_file = os.path.join(project_dir, 'processed_pages.txt')
reviews_base_file = os.path.join(project_dir, 'output.csv')

company = 'Deliveroo'
col_names = ['Company', 'Id', 'Reviewer_Id', 'Title', 'Review', 'Date', 'Rating']
ratings_dict = {1: 'Bad', 2: 'Poor', 3: 'Average', 4: 'Great', 5: 'Excellent'}      

#company_url = '/review/www.deliveroo.co.uk?b=MTYxNDM2ODY0MDAwMHw2MDM5NGY4MGY4NWQ3NTA5ZDhlNWE1N2M'
base_df = pd.read_csv(reviews_base_file, sep=',')
print('Base file has {0} rows and {1} unique Ids'.format(base_df.shape[0], len(base_df['Id'].unique())))

new_reviews_df = pilot.trustPltSniffer(base_domain=source_url, starting_page=company_url,
                      steps=10, processed_urls_f=processed_pages_file,
                      ratings_dict=ratings_dict, col_names=col_names, company_name=company)

base_df_updated = pd.concat([base_df, new_reviews_df], axis=0)
print('Updated base file has {0} rows and {1} unique Ids'.format(base_df_updated.shape[0], len(base_df_updated['Id'].unique())))

base_df_updated.to_csv(reviews_base_file, sep=',', index=False)


pilot.flushLastProcessedPage(processed_urls_f=processed_pages_file, company_name=company)

