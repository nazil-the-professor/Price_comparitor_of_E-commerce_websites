from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time
import random
from difflib import SequenceMatcher

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())  
    return webdriver.Chrome(service=service, options=chrome_options)

def get_amazon_prices(driver, query):
    driver.get(f"https://www.amazon.in/s?k={query}")
    time.sleep(random.uniform(3, 7))  # Randomized sleep to mimic human behavior

    wait = WebDriverWait(driver, 15)
    prices = {}
    reviews = {}
    discounts = {}
    links = {}
    try:
        # Try both class names dynamically for product containers
        product_containers = driver.find_elements(By.CLASS_NAME, "puisg-col-inner")
        if not product_containers:
            product_containers = driver.find_elements(By.CLASS_NAME, 
                "a-section.a-spacing-small.puis-padding-left-small.puis-padding-right-small"
            )

        # print("Amazon Products Found:", len(product_containers))  # Debugging

        for product in product_containers[:5]:  # Limit to first 5 products
            try:
                title = product.find_element(By.TAG_NAME, "h2").text
                
                # Extract price
                price = product.find_element(By.CLASS_NAME, "a-price-whole").text
                prices[title] = int(price.replace(',', ''))
                
                # Extract product link
                link_element = product.find_element(By.TAG_NAME, "a")
                link = link_element.get_attribute("href")
                links[title] = link
                
                # Extract reviews (fixing your issue)
                try:
                    review_element = product.find_element(By.CLASS_NAME, "a-icon-alt")
                    review_text = review_element.get_attribute("innerText").split(" ")[0]  # Extract rating number
                    reviews[title] = float(review_text)
                except Exception:
                    reviews[title] = "No reviews"
                  
                    
                try:
                    span_elements = product.find_elements(By.TAG_NAME, "span")
                    discount_text = "No discount"

                    for span in span_elements:
                        span_text = span.text.strip()
                        if span_text.startswith("(") and "%" in span_text and "off" in span_text:
                            # print(f"Discount found for {title}: {span_text}")  # Debugging
                            discount_text = span_text
                            break

                except NoSuchElementException:
                    print(f"No discount element found for {title}")  # Debugging
                    discount_text = "No discount"
                except Exception as e:
                    print(f"Unexpected error for {title}: {e}")  # Debugging
                    discount_text = "No discount"

                discounts[title] = discount_text

            except Exception:
                continue  # Skip if price/title is not found

    except Exception as e:
        print("Amazon Error:", e)
    
    print("Amazon Links:", links)
    return prices, reviews, discounts,links

  # Return both

def get_flipkart_prices(driver, query):
    driver.get(f"https://www.flipkart.com/search?q={query}")
    time.sleep(random.uniform(3, 6))  # Randomized sleep to mimic human behavior

    wait = WebDriverWait(driver, 10)

    prices = {}
    reviews = {}
    discounts = {}
    links = {}

    try:
        # Wait for products to load
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "slAVV4")))

        # Find all product containers
        product_containers = driver.find_elements(By.CLASS_NAME, "slAVV4")

        if not product_containers:
            print("No products found!")
            return prices, reviews, discounts, links

        for product in product_containers[:5]:  # Limit to first 5 products
            try:
                # Extract title & product link
                try:
                    title_element = product.find_element(By.CLASS_NAME, "wjcEIp")
                    title = title_element.text.strip()
                    link = title_element.get_attribute("href")
                except NoSuchElementException:
                    continue  # Skip if title is missing

                # Extract price
                try:
                    price_element = product.find_element(By.CLASS_NAME, "Nx9bqj")
                    price = price_element.text.replace("₹", "").replace(",", "").strip()
                    prices[title] = int(price)
                except NoSuchElementException:
                    prices[title] = "Price not found"

                # Extract reviews
                try:
                    review_element = product.find_element(By.CLASS_NAME, "XQDdHH")
                    review_text = review_element.text.strip()
                    reviews[title] = float(review_text)
                except NoSuchElementException:
                    reviews[title] = "No reviews"

                # Extract discount
                try:
                    discount_element = product.find_element(By.CLASS_NAME, "UkUFwK")
                    discount_text = discount_element.text.strip()
                    discounts[title] = discount_text
                except NoSuchElementException:
                    discounts[title] = "No discount"

                # Store product link
                links[title] = link if link.startswith("http") else "https://www.flipkart.com" + link

            except Exception:
                continue  # Skip product if any major error occurs

    except TimeoutException:
        print("Timeout: No products found or took too long to load.")

    print("Flipkart Links:", links)
    return prices, reviews, discounts, links

def get_meesho_prices(driver, query):
    driver.get(f"https://www.meesho.com/search?q={query}")
    time.sleep(random.uniform(3, 7))  
    
    wait = WebDriverWait(driver, 15)
    prices = {}
    discounts = {}
    links = {}
    reviews = {}

    try:
        product_containers = driver.find_elements(By.CLASS_NAME, "NewProductCardstyled__CardStyled-sc-6y2tys-0")
        
        for product in product_containers[:5]:  
            try:
                title = product.find_element(By.CLASS_NAME, "NewProductCardstyled__StyledDesktopProductTitle-sc-6y2tys-5").text
                
                # Extract price
                price = product.find_element(By.CLASS_NAME, "sc-eDvSVe.dwCrSh").text.replace("₹", "").strip()
                prices[title] = int(price.replace(',', ''))
                
                # Extract product link
            
                link_element = product.find_element(By.XPATH, ".//ancestor::a")
                link = link_element.get_attribute("href")
                if link and not link.startswith("https"):
                    link = "https://www.meesho.com" + link  # Append base URL if needed
                links[title] = link if link else "No link"
    
                
                # Extract reviews
                try:
                    review_element = product.find_element(By.CLASS_NAME, "jkpPSq")
                    review_text = review_element.text.strip()
                    reviews[title] = float(review_text)
                except:
                    reviews[title] = "No reviews"
                
                # Extract discount information (if available)
                try:
                    discount_elements = product.find_elements(By.XPATH, ".//span[contains(text(), '%')]")
                    if discount_elements:
                        discount_text = discount_elements[0].text
                    else:
                        discount_text = "No discount"
                except Exception:
                    discount_text = "No discount"
                
                discounts[title] = discount_text
                
            except Exception as e:
                print(f"Skipping product due to error: {e}")
                continue  

    except Exception as e:
        print("Meesho Error:", e)
    
    print("Meesho Links:", links)
    return prices, reviews, discounts, links


def get_myntra_prices(driver, query):
    driver.get(f"https://www.myntra.com/{query}")
    time.sleep(random.uniform(3, 7))  # Randomized sleep to mimic human behavior
    
    wait = WebDriverWait(driver, 15)
    prices = {}
    discounts = {}
    links = {}
    reviews = {}
    
    try:
        product_containers = driver.find_elements(By.CLASS_NAME, "product-base")
        
        for product in product_containers[:5]:  # Limit to first 5 products
            try:
                brand = product.find_element(By.CLASS_NAME, "product-brand").text
                name = product.find_element(By.CLASS_NAME, "product-product").text
                title = f"{brand} {name}"
                
                # Extract price
                price = product.find_element(By.CLASS_NAME, "product-discountedPrice").text.replace("Rs. ", "")
                prices[title] = int(price.replace(',', ''))
                
                # Extract product link
                link_element = product.find_element(By.TAG_NAME, "a")
                link = link_element.get_attribute("href")
                links[title] = link
                
                # Extract discount
                try:
                    discount_text = product.find_element(By.CLASS_NAME, "product-discountPercentage").text
                except:
                    discount_text = "No discount"
                
                discounts[title] = discount_text
                try:
                    review_element = product.find_element(By.CLASS_NAME, "product-ratingsContainer")
                    reviews[title] = review_element.text.strip()
                except:
                    reviews[title] = "No reviews"
            except Exception:
                continue  # Skip if price/title is not found

    except Exception as e:
        print("Myntra Error:", e)
    
    print("Myntra Links:", links)
    return prices,reviews, discounts, links

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def compare_prices(request):
    query = request.GET.get('query', '')

    if not query:
        return render(request, 'index.htm', {'error': 'Please enter a product name'})

    driver = get_driver()

    # Fetching prices, reviews, and discounts from each platform
    amazon_prices, amazon_reviews, amazon_discounts, amazon_links = get_amazon_prices(driver, query) # Amazon has no discount section
    flipkart_prices, flipkart_reviews, flipkart_discounts, flipkart_links = get_flipkart_prices(driver, query)
    meesho_prices, meesho_reviews, meesho_discounts, meesho_links = get_meesho_prices(driver, query)
    myntra_prices, myntra_reviews, myntra_discounts, myntra_links = get_myntra_prices(driver, query)

    driver.quit()

    comparisons = []
    
    for amazon_product, amazon_price in amazon_prices.items():
        best_match_flipkart = max(flipkart_prices, key=lambda p: similar(amazon_product.lower(), p.lower()), default=None)
        best_match_meesho = max(meesho_prices, key=lambda p: similar(amazon_product.lower(), p.lower()), default=None)
        best_match_myntra = max(myntra_prices, key=lambda p: similar(amazon_product.lower(), p.lower()), default=None)
        
        print(f"Best Match Flipkart: {best_match_flipkart}")
        price_dict = {
            "Amazon": amazon_price,
            "Flipkart": flipkart_prices.get(best_match_flipkart, float('inf')),
            "Meesho": meesho_prices.get(best_match_meesho, float('inf')),
            "Myntra": myntra_prices.get(best_match_myntra, float('inf'))
        }

        cheapest_store = min(price_dict, key=lambda k: price_dict[k] if isinstance(price_dict[k], (int, float)) else float('inf'))

        comparisons.append({
            'product': amazon_product,
            'amazon_price': amazon_price,
            'flipkart_price': flipkart_prices.get(best_match_flipkart, "Not Found"),
            'meesho_price': meesho_prices.get(best_match_meesho, "Not Found"),
            'myntra_price': myntra_prices.get(best_match_myntra, "Not Found"),
            
            'amazon_reviews': amazon_reviews.get(amazon_product, "No reviews"),
            'flipkart_reviews': flipkart_reviews.get(best_match_flipkart, "No reviews") if isinstance(flipkart_reviews, dict) else "No reviews",
            'meesho_reviews': meesho_reviews.get(best_match_meesho, "No reviews") if isinstance(meesho_reviews, dict) else "No reviews",
            'myntra_reviews': myntra_reviews.get(best_match_myntra, "No reviews") if isinstance(myntra_reviews, dict) else "No reviews",

            'amazon_discount': amazon_discounts.get(amazon_product, "No discount"),      
            'flipkart_discount': flipkart_discounts.get(best_match_flipkart, "No discount"),
            'meesho_discount': meesho_discounts.get(best_match_meesho, "No discount"),
            'myntra_discount': myntra_discounts.get(best_match_myntra, "No discount"),
            
            'amazon_link': amazon_links.get(amazon_product, "#"),
            'flipkart_link': flipkart_links.get(best_match_flipkart, "#") if best_match_flipkart else "#",
            'meesho_link': meesho_links.get(best_match_meesho, "#"),
            'myntra_link': myntra_links.get(best_match_myntra, "#"),
            
            'cheaper_on': cheapest_store
        })

    return render(request, 'result.htm', {'comparisons': comparisons})



def Result(request):
    return render(request, 'result.htm')


def welcome(request):
    return render(request, 'welcome.htm')