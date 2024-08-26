import requests
import csv

# Base URL for fetching reviews
base_url = "https://itunes.apple.com/us/rss/customerreviews/page={}/id={}/sortBy=mostRecent/json"

def get_raw_reviews(app_id="431156417", num_pages=2):
    # Application ID and number of pages to fetch

    # Opening CSV file for writing with utf-8-sig encoding
    with open('app_store_reviews.csv', mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        # Writing the header
        writer.writerow(["Title", "Review", "Date", "Rating"])
    
        # Loop through the pages
        for page in range(1, num_pages + 1):
            # Fetching the data from the current page
            response = requests.get(base_url.format(page, app_id))
            data = response.json()
    
            # Parsing the reviews
            reviews = data['feed'].get('entry', [])
    
            # Writing the review data
            for review in reviews:
                title = review['title']['label']
                review_content = review['content']['label']
                date = review['updated']['label']
                rating = review['im:rating']['label']
    
                writer.writerow([title, review_content, date, rating])
    
            print(f"Page {page} processed.")
    
    print("CSV file has been created successfully.")