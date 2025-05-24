import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from snowflake.snowpark.context import get_active_session
import plotly.graph_objects as go
import json
from PIL import Image
import random
#import base64
#from io import BytesIO

# Set page configuration - must be the first Streamlit command
st.set_page_config(
    page_title="India Tourism Insights Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.write("By TamilRock Stars")
    
st.markdown(
    """
    <style>
    /* Visually attractive H1 with gradient, shadow, and animation */
    .fancy-title {
        background: linear-gradient(90deg, #00c6ff, #0072ff, #00c6ff);
        background-size: 200% auto;
        color: transparent;
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Arial Black', Arial, sans-serif;
        font-size: 3rem;
        letter-spacing: 3px;
        text-align: center;
        margin-bottom: 32px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        animation: shine 3s linear infinite;
    }
    @keyframes shine {
        to {
            background-position: 200% center;
        }
    }
    /* Container for images: fixed square boxes with responsive layout */
    .image-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin: 0 auto;
        max-width: 820px;
    }
    .image-box {
        position: relative;
        width: 100%;
        padding-top: 100%; /* 1:1 Aspect Ratio */
        overflow: hidden;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.10);
        transition: box-shadow 0.3s, transform 0.3s;
        cursor: pointer;
        background: linear-gradient(135deg, #e0f7fa 0%, #ffffff 100%);
    }
    .image-box:hover {
        box-shadow: 0 8px 32px rgba(0,0,0,0.18);
        transform: scale(1.04);
        z-index: 1;
    }
    .image-box img {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 100%;
        height: 100%;
        object-fit: cover;
        transform: translate(-50%, -50%);
        border-radius: 16px;
        transition: transform 0.4s;
    }
    .image-box:hover img {
        transform: translate(-50%, -50%) scale(1.10);
    }
    </style>

    # :blue[Welcome to the India Tourism Insights Dashboard]

    ## :orange[Discover the beauty and diversity of India!]

    ---
    
    :green[Explore] the vibrant culture, :red[stunning landscapes], and :violet[rich heritage]  
    through our comprehensive insights and data visualizations.

    ### Why choose our dashboard?

    - :sparkles: **Interactive and intuitive** interface  
    - :bar_chart: **Data-driven** insights for smarter travel planning  
    - :earth_asia: Covers all major tourist destinations across India  

    > :blue[“Travel is the only thing you buy that makes you richer.”]

    ---
    
    
 <h3 style="color: violet; text-align: center;">
        <b>Start your journey with us today and unlock the secrets of Incredible India!</b>
    </h3>
    """,
    unsafe_allow_html=True
)


# Initialize Snowflake session
session = get_active_session()



# Load data from Snowflake
@st.cache_data
def load_data():
    df = session.table("TOURISM_DB.TOURISM_SCHEMA.TOURISM_DATA").to_pandas()
    return df

df = load_data()

# Load the GeoJSON for Indian states
@st.cache_data
def load_geojson():
    with open("india_states.geojson") as response:
        geojson = json.load(response)
    return geojson

geojson = load_geojson()

# List of all Indian states from the geojson (to match codes)
states = [feature['properties']['NAME_1'] for feature in geojson['features']]

#Color Selection col 5
color_palette = ["#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9", "#92A8D1", "#955251", "#B565A7", "#009B77"]
random.shuffle(color_palette)

#Toursiam sites
tourism_sites = [
    "incredibleindia.org",
    "www.luxurytraveladvisor.com",
    "www.tripadvisor.in/",
    "www.sotc.in/",
    "www.responsibletravel.com",
    "www.indiatravel.com/",
    "makemytrip.com",
    "www.thomascook.in/india-tourism",
    "www.semrush.com/trending-websites/in/travel-and-tourism",
    "www.yatra.com/india-tourism",
    "www.tourmyindia.com",
    "www.holidify.com/country/india/",
    "www.incredibleindia.gov.in/en",
    "www.irctctourism.com/",
]

# Define the tourism information for each state
india_tourism_info = {
    "Andhra Pradesh": {
        "Top 10 Must-Visit Places": [
            {"name": "Tirumala Tirupati Devasthanams (Tirupati)", "image_url": r"Images/Andhra/Tirupathi.jpg"},
            {"name": "Araku Valley", "image_url": r"Images/Andhra/ArakuValley.jpg"},
            {"name": "Borra Caves", "image_url": r"Images/Andhra/Borra-Cave.jpg"},
            {"name": "Visakhapatnam (Vizag): R.K. Beach, Kailasagiri", "image_url": r"Images/Andhra/Visakhapatnam.jpg"},
            {"name": "Chilika Lake", "image_url": r"Images/Andhra/Chilika-Lake.png"},
            {"name": "Sri Kalahasti Temple", "image_url": r"Images/Andhra/kalahasteeswaraSwami.jpg"},
            {"name": "Nellore: Penchalakona", "image_url": r"Images/Andhra/Temple.jpg"},
            {"name": "Kondapalli Fort", "image_url": r"Images/Andhra/KondapalliFor.jpg"},
            {"name": "Ponduru: Famous for Handloom and Silk", "image_url": r"Images/Andhra/Ponduru.jpg"},
        ],
        "Best Season to Visit": "October to March (Winter and early Spring)"
    },
    "Tamil Nadu": {
        "Top 10 Must-Visit Places": [
            {"name": "Chennai (Marina Beach)", "image_url": r"Images/TN/marina-beach-chennai.jpg"},
            {"name": "Madurai (Meenakshi Temple)", "image_url": r"Images/TN/Meenakshi.jpg"},
            {"name": "Vellore (Golden Temple)", "image_url": r"Images/TN/vellore_t.jpg"},
            {"name": "Thanjavur (Brihadeeswarar Temple)", "image_url": r"Images/TN/thanjavur.jpg"},
            {"name": "Tiruchirappalli", "image_url": r"Images/TN/Tiruchirappalli.jpg"},
            {"name": "Rameswaram", "image_url": r"Images/TN/pambann.jpg"},
            {"name": "Mahabalipuram", "image_url": r"Images/TN/Mahabalipuram.jpg"},
            {"name": "Coimbatore", "image_url": r"Images/TN/Coimbatore.jpg"},
            {"name": "Kodaikanal", "image_url": r"Images/TN/kodaikanl.jpg"},
        ],
        "Best Season to Visit": "October to March (Winter and early Spring)"
    },
    
    # Add more states here...
    "Manipur": {
        "Top 10 Must-Visit Places": [
            {"name": "Imphal", "image_url": r"Images/Manipur/Imphal_image.jpg"},
            {"name": "Loktak Lake", "image_url": r"Images/Manipur/Loktak_Lake_image.jpg"},
            {"name": "Kangla Fort", "image_url": r"Images/Manipur/Kangla_Fort_image.jpg"},
            {"name": "Shree Shree Govindajee Temple", "image_url": r"Images/Manipur/Shree_Shree_Govindajee_Temple_image.jpg"},
            {"name": "Keibul Lamjao National Park", "image_url": r"Images/Manipur/Keibul_Lamjao_National_Park_image.jpg"},
            {"name": "Manipur State Museum", "image_url": r"Images/Manipur/Manipur State_Museum_image.jpg"},
            {"name": "Senapati", "image_url": r"Images/Manipur/Senapati_image.jpg"},
            {"name": "Ukhrul", "image_url": r"Images/Manipur/Manipur_image.jpg"},
            {"name": "Khongjom War Memorial", "image_url": r"Images/Manipur/Khongjom_War_Memorial_image.jpg"},
        ],
        "Best Season to Visit": "October to March (Winter)"
    },

    #Mizoram
    "Mizoram": {
        "Top 10 Must-Visit Places": [
            {"name": "Aizawl", "image_url": r"Images/Mizoram/Aizawl_image.jpg"},
            {"name": "Lunglei", "image_url": r"Images/Mizoram/Lunglei_image.jpg"},
            {"name": "Tualvawng", "image_url": r"Images/Mizoram/Tualvawng_image.jpg"},
            {"name": "Sailani", "image_url": r"Images/Mizoram/Sailani_image.jpg"},
            {"name": "Vantawng Falls", "image_url": r"Images/Mizoram/Vantawng_Falls_image.jpg"},
            {"name": "Reiek", "image_url": r"Images/Mizoram/Reiek_image.jpg"},
            {"name": "Phawngpui Blue Mountain", "image_url": r"Images/Mizoram/Phawngpui_Blue.jpg"},
            {"name": "Champhai", "image_url": r"Images/Mizoram/Champhai_image.jpg"},
            {"name": "Thenzawl", "image_url": r"Images/Mizoram/Thenzawl_image.jpg"},
        ],
        "Best Season to Visit": "March to June (Summer) or September to November (Post-monsoon)"
    },
    
    #Nagaland
    "Nagaland": {
        "Top 10 Must-Visit Places": [
            {"name": "Kohima", "image_url": r"Images/Nagaland/Kohima_image.jpg"},
            {"name": "Dimapur", "image_url": r"Images/Nagaland/Dimapur_image.jpg"},
            {"name": "Dzukou Valley", "image_url": r"Images/Nagaland/Dzukou Valley_image.jpg"},
            {"name": "Mokokchung", "image_url": r"Images/Nagaland/Mokokchung_image.jpg"},
            {"name": "Shilloi Lake", "image_url": r"Images/Nagaland/Shilloi_Lake_image.jpg"},
            {"name": "Chümoukedima", "image_url": r"Images/Nagaland/Chümoukedima_image.jpg"},
            {"name": "Pulie Badze", "image_url": r"Images/Nagaland/1659476263images.jpeg"},
            {"name": "Naga Heritage Village", "image_url": r"Images/Nagaland/Naga_Heritage Village_image.jpg"},
            {"name": "Intangki National Park", "image_url": r"Images/Nagaland/Intangki_National Park_image.jpg"},
        ],
        "Best Season to Visit": "March to June (Summer) or September to November (Post-monsoon)"
    },
    #Odisha

    "Odisha": {
        "Top 10 Must-Visit Places": [
            {"name": "Konark Sun Temple", "image_url": r"Images/Odisha/Konarka_Temple.jpg"},
            {"name": "Puri Beach", "image_url": r"Images/Odisha/Puri_Beach_imag.jpg"},
            {"name": "Chilika Lake", "image_url": r"Images/Odisha/Chilika_Lake_image.jpg"},
            {"name": "Bhubaneswar", "image_url": r"Images/Odisha/Bhubaneswar_image.jpg"},
            {"name": "Nandankanan Zoo", "image_url": r"Images/Odisha/NandankananZoo_image.jpg"},
            {"name": "Jagannath Temple", "image_url": r"Images/Odisha/Jagannath_Temple_image.jpg"},
            {"name": "Simlipal National Park", "image_url": r"Images/Odisha/Simlipal_National_Park_imaghe.jpg"},
            {"name": "Raghurajpur Village", "image_url": r"Images/Odisha/Raghurajpur_Village_image.jpg"},
            {"name": "Cuttack", "image_url": r"Images/Odisha/Cuttack_image.jpg"},
        ],
        "Best Season to Visit": "October to March (Winter)"
    },

    #Punjab
     "Punjab": {
        "Top 10 Must-Visit Places": [
            {"name": "Golden Temple (Amritsar)", "image_url": r"Images/Punjab/Golden_Temple_image.jpg"},
            {"name": "Jallianwala Bagh", "image_url": r"Images/Punjab/Jallianwala_Bagh_image.jpg"},
            {"name": "Wagah Border", "image_url": r"Images/Punjab/Wagah_Border_image.jpg"},
            {"name": "Durgiana Temple", "image_url": r"Images/Punjab/Durgiana_Temple_image.jpg"},
            {"name": "Harmandir Sahib", "image_url": r"Images/Punjab/Harmandir_Sahib_image.jpg"},
            {"name": "Anandpur Sahib", "image_url": r"Images/Punjab/AnandpurSahib_image.jpg"},
            {"name": "Ropar Wetland", "image_url": r"Images/Punjab/Ropar_Wetland_image.jpg"},
            {"name": "Khalsa College", "image_url": r"Images/Punjab/Khalsa_College_image.jpg"},
            {"name": "Patiala", "image_url": r"Images/Punjab/Patiala_image.jpg"},
        ],
        "Best Season to Visit": "March to June (Summer) or September to November (Post-monsoon)"
    },

    #Rajasthan

    "Rajasthan": {
        "Top 10 Must-Visit Places": [
            {"name": "Jaipur (Amber Fort, Hawa Mahal)", "image_url": r"Images/Rajasthan/Hawa-mahal.jpg"},
            {"name": "Jodhpur (Mehrangarh Fort)", "image_url": r"Images/Rajasthan/Jodhpur_image.jpg"},
            {"name": "Udaipur (Lake Palace)", "image_url": r"Images/Rajasthan/Udaipur_image.jpg"},
            {"name": "Jaisalmer (Golden Fort)", "image_url": r"Images/Rajasthan/Jaisalmer _image.jpg"},
            {"name": "Pushkar", "image_url": r"Images/Rajasthan/Pushkar_image.jpg"},
            {"name": "Mount Abu", "image_url": r"Images/Rajasthan/Mount_Abu_image.jpg"},
            {"name": "Chittorgarh Fort", "image_url": r"Images/Rajasthan/Chittorgarh_Fort_image.jpg"},
            {"name": "Bikaner (Junagarh Fort)", "image_url": r"Images/Rajasthan/Bikaner_(Junagarh Fort).jpg"},
            {"name": "Ranthambore National Park", "image_url": r"Images/Rajasthan/Ranthambore_National_Park_image.jpg"},
        ],
        "Best Season to Visit": "October to March (Winter)"
    },


    #Sikkim
    "Sikkim": {
        "Top 10 Must-Visit Places": [
            {"name": "Gangtok", "image_url": r"Images/Sikkim/Gangtok_image.jpg"},
            {"name": "Tsongmo Lake", "image_url": r"Images/Sikkim/tsomgo-lake.jpg"},
            {"name": "Nathu La Passr", "image_url": r"Images/Sikkim/Nathula_pass.jpg"},
            {"name": "Pellling", "image_url": r"Images/Sikkim/pelling.jpg"},
            {"name": "Rumtek Monastery", "image_url": r"Images/Sikkim/images_Rumtek_Monastery.jpg"},
            {"name": "Yuksom", "image_url": r"Images/Sikkim/Yuksom_image.jpg"},
            {"name": "Khangchendzonga National Park", "image_url": r"Images/Sikkim/khangchendzong_national_park1.jpg"},
            {"name": "Zuluk", "image_url": r"Images/Sikkim/Zuluk_image.jpg"},
            {"name": "Singalila National Park", "image_url": r"Images/Sikkim/Gangtok_Tsomgo_Lake_Main.jpg"},
        ],
        "Best Season to Visit": "March to June and September to December (Summer and Autumn)"
    },

    #ArunachalP
    "Arunachal Pradesh": {
        "Top 10 Must-Visit Places": [
            {"name": "Tawang Monastery", "image_url": r"Images/Arunachal/tawang-monastery.jpg"},
            {"name": "Sela Pass", "image_url": r"Images/Arunachal/arunachal-pradesh.jpg"},
            {"name": "Ziro Valley", "image_url": r"Images/Arunachal/Ziro-Valley-Arunachal.jpg"},
            {"name": "Dirang", "image_url": r"Images/Arunachal/Mechuka_Valley.jpg"},
            {"name": "Namdapha National Park", "image_url": r"Images/Arunachal/Namdapha_National_Park.jpg"},
            {"name": "Itanagar", "image_url": r"Images/Arunachal/ITANAGAR.jpg"},
            {"name": "Bhalukpong", "image_url": r"Images/Arunachal/Bhalukpong.jpg"},
            #{"name": "Bomdila", "image_url": r" "},
            {"name": "Monpa Village", "image_url": r"Images/Arunachal/Monpa_Village.jpg"},
        ],
        "Best Season to Visit": "March to June (Summer) or September to November (Post-monsoon)"
    },

    #Assam
    "Assam": {
        "Top 10 Must-Visit Places": [
            {"name": "Kaziranga National Park", "image_url": r"Images/assam/Kaziranga_NationalPark.jpg"},
            {"name": "Majuli Island", "image_url": r"Images/assam/Majuli_Island.jpg"},
            {"name": "Kamakhya Temple", "image_url": r"Images/assam/Kamakhya_Temple_Attractions.jpg"},
            {"name": "Tea Gardens in Jorhat", "image_url": r"Images/assam/Tea_Gardens_inJorhat.jpg"},
            {"name": "Manas National Park", "image_url": r"Images/assam/Manas_National_Park.jpg"},
            {"name": "Sivasagar", "image_url": r"Images/assam/Sivasagar.jpg"},
            {"name": "Haflong", "image_url": r"Images/assam/haflong_Rajat-Agarwa.jpg"},
            {"name": "Umananda Temple", "image_url": r"Images/assam/Umananda_Temple.jpg"},
            {"name": "Nameri National Park", "image_url": r"Images/assam/Nameri_National_Park.jpg"},
        ],
        "Best Season to Visit": "March to June (Summer) or September to November (Post-monsoon)"
    },

    #Bihar
    "Bihar": {
        "Top 10 Must-Visit Places": [
            {"name": "Nalanda University Ruins", "image_url": r"Images/Bihar/Nalanda_University_Ruins.jpg"},
            {"name": "Mahabodhi Temple (Bodh Gaya)", "image_url": r"Images/Bihar/Mahabodhi_Temple_.jpg"},
            {"name": "Patna Museum", "image_url": r"Images/Bihar/Patna_Museum.jpg"},
            {"name": "Vikramshila University Ruins", "image_url": r"Images/Bihar/Vikramshila_University_Ruins.jpg"},
            {"name": "Kumhrar Ruins", "image_url": r"Images/Bihar/Kumhrar_Ruin.jpg"},
            {"name": "Vaishali (Ancient Buddhist site)", "image_url": r"Images/Bihar/Vaishali.jpg"},
            {"name": "Barabar Caves", "image_url": r"Images/Bihar/Barabar_Caves.jpg"},
            {"name": "Madhubani (Famous for Madhubani paintings)", "image_url": r"Images/Bihar/Madhubani.jpg"},
            {"name": "Sonepur Mela", "image_url": r"Images/Bihar/sonepur-mela2.jpg"},
        ],
        "Best Season to Visit": "October to March (Winter)"
    },


    #Goa
    "Goa": {
        "Top 10 Must-Visit Places": [
            {"name": "Baga Beach", "image_url": r"Images/goa/Baga-Beach.jpg"},
            {"name": "Anjuna Beach", "image_url": r"Images/goa/Anjuna_Beach.jpg"},
            {"name": "Basilica of Bom Jesus", "image_url": r"Images/goa/Basilica_of_Bom_Jesus.jpg"},
            {"name": "Dudhsagar Waterfalls", "image_url": r"Images/goa/Dudhsagar_Waterfalls.jpg"},
            {"name": "Fort Aguada", "image_url": r"Images/goa/Fort_Aguada.jpg"},
            {"name": "Church of St. Cajetan", "image_url": r"Images/goa/Church_of_St._Cajetan.jpg"},
            {"name": "Palolem Beach", "image_url": r"Images/goa/Palolem_Beach.jpg"},
            {"name": "Colva Beach", "image_url": r"Images/goa/Colva_Beach.jpg"},
            {"name": "Goa State Museum", "image_url": r"Images/goa/Goa_State_Museum.jpg"},
        ],
        "Best Season to Visit": "November to February (Winter)"
    },


    #Gujarat
    "Gujarat": {
        "Top 10 Must-Visit Places": [
            {"name": "Rann of Kutch (Rann Utsav)", "image_url": r"Images/Gujarat/Rann-Utsav-at-Rann-of-Kutch.jpg"},
            {"name": "Gir National Park", "image_url": r"Images/Gujarat/Gir_National_Park.jpg"},
            {"name": "Somnath Temple", "image_url": r"Images/Gujarat/Somnath _emple.jpg"},
            {"name": "Dwarka", "image_url": r"Images/Gujarat/Dwarka.jpg"},
            {"name": "Kankaria Lake", "image_url": r"Images/Gujarat/Kankaria_Lake.jpg"},
            {"name": "Sabarmati Ashram", "image_url": r"Images/Gujarat/Sabarmati_Ashram.jpg"},
            {"name": "Statue of Unity", "image_url": r"Images/Gujarat/Statue_of_Unity.jpg"},
            {"name": "Vadodara (Laxmi Vilas Palace)", "image_url": r"Images/Gujarat/Vadodara.jpg"},
            {"name": "Lothal", "image_url": r"Images/Gujarat/Lothal.jpg"},
        ],
        "Best Season to Visit": "October to March (Winter)"
    },

    #Haryana
    "Haryana": {
        "Top 10 Must-Visit Places": [
            {"name": "Kurukshetra", "image_url": r"Images/Haryana/Kurukshetra_Plac.jpg"},
            {"name": "Sultanpur Bird Sanctuary", "image_url": r"Images/Haryana/Sultanpur_Bird_Sanctuary.jpg"},
            {"name": "Pinjore Gardens", "image_url": r"Images/Haryana/Pinjore_Gardens.jpg"},
            {"name": "Faridabad", "image_url": r"Images/Haryana/Faridabad.jpg"},
            {"name": "Damdama Lake", "image_url": r"Images/Haryana/Damdama_Lake.jpg"},
            {"name": "Baba Farid's Tomb", "image_url": r"Images/Haryana/Baba_Bandha_Singh.jpg"},
            {"name": "Chattbir Zoo", "image_url": r"Images/Haryana/Chattbir_Zoo.jpg"},
            {"name": "Surajkund", "image_url": r"Images/Haryana/Surajkund-Mela-2022.jpeg"},
            {"name": "Gurgaon ", "image_url": r"Images/Haryana/Gurgaon.jpg"},
        ],
        "Best Season to Visit": "October to March (Winter)"
    },


    #Himachal Prades
    "Himachal Pradesh": {
        "Top 10 Must-Visit Places": [
            {"name": "Shimla", "image_url": r"Images/Himachal/Shimla.jpg"},
            {"name": "Manali", "image_url": r"Images/Himachal/chamba-valley.jpg"},
            {"name": "Dharamshala", "image_url": r"Images/Himachal/DHARAMSHALA.jpg"},
            {"name": "Kullu Valley", "image_url": r"Images/Himachal/Kullu_Valley.jpg"},
            {"name": "Spiti Valley", "image_url": r"Images/Himachal/Kullu_Valley.jpg"},
            {"name": "Kangra Fort", "image_url": r"Images/Himachal/Kangra-Fort1.jpg"},
            {"name": "Dalhousie", "image_url": r"Images/Himachal/Dalhousie.jpg"},
            {"name": "Kasauli", "image_url": r"Images/Himachal/Kasauli.jpg"},
            {"name": "Tirthan Valley", "image_url": r"Images/Himachal/Tirthan_Valley.jpg"},
        ],
        "Best Season to Visit": "March to June (Summer) or December to February (Winter for snow activities)"
    },


    #Jharkhand
    "Jharkhand": {
        "Top 10 Must-Visit Places": [
            {"name": "Ranchi (Tagore Hill, Rock Garden)", "image_url": r"Images/Jharkhand/Maithon_Dam.jpg"},
            {"name": "Jamshedpur", "image_url": r"Images/Jharkhand/Jamshedpur_Attractions.jpg"},
            {"name": "Hazaribagh National Park", "image_url": r"Images/Jharkhand/Hazaribagh_National_Park.jpg"},
            {"name": "Betla National Park", "image_url": r"Images/Jharkhand/betla-national-park.jpg"},
            {"name": "Dassam Falls", "image_url": r"Images/Jharkhand/Dassam_Falls.png"},
            {"name": "Maithon Dam", "image_url": r"Images/Jharkhand/Maithon_Dam.jpg"},
            {"name": "Sun Temple, Deoghar", "image_url": r"Images/Jharkhand/Sun_Temple.jpg"},
            {"name": "Rajrappa Temple", "image_url": r"Images/Jharkhand/Rajrappa-Mandir.jpg"},
            {"name": "Jonha Falls", "image_url": r"Images/Jharkhand/Jonha_Falls_Attractions.jpg"},
        ],
        "Best Season to Visit": "March to June (Summer) or September to November (Post-monsoon)"
    },


    #Telangana
    "Telangana": {
        "Top 10 Must-Visit Places": [
            {"name": "Hyderabad (Charminar, Golconda Fort)", "image_url": r"Images/Telangana/Hyderabad_Charminar.jpg"},
            {"name": "Warangal", "image_url": r"Images/Telangana/Warangal.jpg"},
            {"name": "Bhadrachalam", "image_url": r"Images/Telangana/Bhadrachalam.jpg"},
            {"name": "Nizamabad", "image_url": r"Images/Telangana/Nizamabad.jpg"},
            {"name": "Khammam", "image_url": r"Images/Telangana/Khammam.jpg"},
            {"name": "Srisailam", "image_url": r"Images/Telangana/Srisailam.jpg"},
            {"name": "Pochampally", "image_url": r"Images/Telangana/Pochampally.jpg"},
            {"name": "Adilabad", "image_url": r"Images/Telangana/Adilabad.jpg"},
            {"name": "Ramoji Film City", "image_url": r"Images/Telangana/Ramoji Film City.jpg"},
        ],
        "Best Season to Visit": "March to June (Summer) or September to November (Post-monsoon)"
    },


    #Uttar Pradesh
    "Uttar Pradesh": {
        "Top 10 Must-Visit Places": [
            {"name": "Taj Mahal (Agra)", "image_url": r"Images/Uttar_pradesh/Sarnath.jpg"},
            {"name": "Varanasi (Kashi Vishwanath Temple)", "image_url": r"Images/Uttar_pradesh/Varanasi_(Kashi_Vishwanath_Temple).jpg"},
            {"name": "Fatehpur Sikri", "image_url": r"Images/Uttar_pradesh/Fatehpur_Sikr.jpg"},
            {"name": "Vrindavan", "image_url": r"Images/Uttar_pradesh/Vrindavan.jpg"},
            {"name": "Mathura", "image_url": r"Images/Uttar_pradesh/Mathura.jpg"},
            {"name": "Allahabad (Prayagraj Kumbh Mela)", "image_url": r"Images/Telangana/Srisailam.jpg"},
            {"name": "Lucknow (Bada Imambara)", "image_url": r"Images/Uttar_pradesh/Lucknow_(Bada Imambara).jpg"},
            {"name": "Ayodhya", "image_url": r"Images/Uttar_pradesh/Ayodhya.jpg"},
            {"name": "Kanpur", "image_url": r"Images/Telangana/Ramoji Film City.jpg"},
        ],
        "Best Season to Visit": "March to June (Summer) or September to November (Post-monsoon)"
    },


    #Tripura
    "Tripura": {
        "Top 10 Must-Visit Places": [
            {"name": "Agartala", "image_url": r"Images/Tripura/Agartala.jpg"},
            {"name": "Ujjayanta Palace", "image_url": r"Images/Tripura/Ujjayanta_Palace.jpg"},
            {"name": "Neermahal Palace", "image_url": r"Images/Tripura/Neermahal_Palace.jpg"},
            {"name": "Sepahijala Wildlife Sanctuary", "image_url": r"Images/Tripura/Sepahijala_Wildlife_Sanctuary.jpg"},
            {"name": "Trishna Wildlife Sanctuary", "image_url": r"Images/Tripura/Trishna_Wildlife_Sanctuary.jpg"},
            {"name": "Jagannath Temple", "image_url": r"Images/Tripura/Jagannath_Temple.jpg"},
            {"name": "Radhakishore Manikya Museum", "image_url": r"Images/Tripura/Radhakishore_Manikya_Museum.jpg"},
            {"name": "Bhubaneshwar Temple", "image_url": r"Images/Tripura/Bhubaneshwar_Temple.jpg"},
            {"name": "Dumboor Lake", "image_url": r"Images/Tripura/Dumboor_Lake.jpg"},
        ],
        "Best Season to Visit": "October to March (Winter)"
    },


     #Uttarakhand
    "Uttarakhand": {
        "Top 10 Must-Visit Places": [
            {"name": "Dehradun", "image_url": r"Images/Uttarakhand/Dehradun.jpg"},
            {"name": "Mussoorie", "image_url": r"Images/Uttarakhand/Mussoorie.jpg"},
            {"name": "Nainital", "image_url": r"Images/Uttarakhand/Auli.jpg"},
            {"name": "Haridwar", "image_url": r"Images/Uttarakhand/Haridwar.jpg"},
            {"name": "Rishikesh", "image_url": r"Images/Uttarakhand/Rishikesh.jpg"},
            {"name": "Jim Corbett National Park", "image_url": r"Images/Uttarakhand/Jim_Corbett_National_Park.jpg"},
            {"name": "Badrinath Temple", "image_url": r"Images/Uttarakhand/Badrinath_Temple.jpg"},
            {"name": "Kedarnath", "image_url": r"Images/Uttarakhand/Kedarnath.jpg"},
            {"name": "Rudraprayag", "image_url": r"Images/Uttarakhand/Rudraprayag.jpg"},
        ],
        "Best Season to Visit": "March to June and September to November (Summer and Autumn)"
    },


     #West Bengal
    "West Bengal": {
        "Top 10 Must-Visit Places": [
            {"name": "Kolkata", "image_url": r"Images/West Bengal/Kolkata.jpg"},
            {"name": "Sundarbans National Park", "image_url": r"Images/West Bengal/Sundarbans_National_Park.jpg"},
            {"name": "Darjeeling", "image_url": r"Images/West Bengal/Darjeeling.jpg"},
            {"name": "Shantiniketan", "image_url": r"Images/West Bengal/Shantiniketan.jpg"},
            {"name": "Kalimpong", "image_url": r"Images/West Bengal/Kalimpong.jpg"},
            {"name": "Digha", "image_url": r"Images/West Bengal/Digha.jpg"},
            {"name": "Murshidabad", "image_url": r"Images/West Bengal/Murshidabad.jpg"},
            {"name": "Jalpaiguri", "image_url": r"Images/West Bengal/Jalpaiguri.jpg"},
            {"name": "Tajpur Beach", "image_url": r"Images/West Bengal/Tajpur_Beach.jpg"},
        ],
        "Best Season to Visit": "October to March (Winter)"
    },

    
}


# Affordable Price Hotels 
india_Hotel_info = {
    "Andhra Pradesh": {
        "Top Affordable Hotels": [
            {"hotel_name": "The Leela Palace ", "image_url": r"hotels/LeelaHotel.jpg"},
            {"hotel_name": "Lemon Tree Hotels", "image_url": r"hotels/LemonTree.jpg"},
            {"hotel_name": "Radisson Hotels", "image_url": r"hotels/radison.jpg"},
            {"hotel_name": "Hyatt Hotels: R.K. Beach, Kailasagiri", "image_url": r"hotels/Hyatt_Hotel.jpg"},
            {"hotel_name": "AccorHotels", "image_url": r"hotels/AccorHotels.jpg"},
            {"hotel_name": "The Oberoi Group", "image_url": r"hotels/oberi.jpg"},
            {"hotel_name": "Marriott Hotels", "image_url": r"hotels/MarriottHotels.jpg"},
            {"hotel_name": "ITC Hotels", "image_url": r"hotels/ITCHotels.png"},
            {"hotel_name": "Taj Hotels: Famous for Handloom and Silk", "image_url": r"hotels/taj.jpg"},
        ],
        #"Best Season to Visit": "October to March (Winter and early Spring)" www.luxurytraveladvisor.com
    },
   
}

# Sidebar filters for tourism insights
state = st.sidebar.selectbox("Select State/UT", sorted(df["STATE_UT"].unique()))
year = st.sidebar.selectbox("Select Year", sorted(df["YEAR"].unique(), reverse=True))



# Filter data based on selections
filtered_df = df[(df["STATE_UT"] == state) & (df["YEAR"] == year)]

#Main Dashboard Dropdown
col1, col2, col3 = st.columns([2, 2, 1])
with col3:
    dropdown_option = st.selectbox(
        "See it in Your Filter View", 
        ["Indian Tourist Places", "Top Affordable Hotels", "Tourism Metrics 2021-22"]
    )

# Filter your DataFrame
filtered_df = df[(df["STATE_UT"] == state) & (df["YEAR"] == year)]

# Custom CSS for dropdown with hover behavior and enhanced label
st.markdown("""
<style>
/* Dropdown container */
.stSelectbox {
    position: relative;
    display: inline-block;
    font-family: 'Segoe UI', sans-serif;
}

/* Dropdown trigger (selectbox input area) */
.stSelectbox > div[data-baseweb="select"] > div {
    background-color: #f1f1f1;
    padding: 10px 16px;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    transition: 0.3s;
}

/* Dropdown content (listbox) */
.stSelectbox div[role="listbox"] {
    display: none;
    position: absolute;
    background-color: #2F4F4F; /* Dark slate gray for dark theme */
    min-width: 240px;
    max-height: 200px;
    overflow-y: auto;
    border: 1px solid #ddd;
    z-index: 1;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3); /* Stronger shadow for dark theme */
    border-radius: 4px;
    padding: 10px;
}

/* Show dropdown content on hover */
.stSelectbox:hover div[role="listbox"] {
    display: block;
}

/* Dropdown option styling */
.stSelectbox div[role="option"] {
    padding: 8px 10px;
    cursor: pointer;
    color: #E0E0E0; /* Light gray text for readability on dark background */
}

/* Dropdown option hover effect */
.stSelectbox div[role="option"]:hover {
    background-color: #4682B4; /* Steel blue for hover effect */
}

/* Label styling for enhanced visibility */
.stSelectbox label {
    font-weight: 700;
    font-size: 18px;
    color: #F5F5F5; /* Off-white for contrast on dark background */
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5); /* Subtle shadow for depth */
    margin-bottom: 8px;
    display: block;
}

/* Placeholder text */
.css-1wa3eu0-placeholder {
    color: #A9A9A9 !important; /* Light gray for placeholder */
    font-style: italic;
}

/* Overall page style */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    color: #E0E0E0; /* Light text for dark theme */
}
</style>
""", unsafe_allow_html=True)


#Filter 1 

if dropdown_option == "Indian Tourist Places":
    st.subheader(f"Tourism Metrics for {state}")
    st.write("👈 Filter Your Favorite States Side Bar")
    # Show Top 10 Must-Visit Places images in 3 columns responsive grid
    if state:
        state_info = india_tourism_info.get(state)
        if state_info:
            st.markdown(f"### Welcome to {state}")
            st.markdown(f"**Best Season to Visit:** {state_info['Best Season to Visit']}")
            st.markdown("### Top 10 Must-Visit Places:")
            cols = st.columns(3)
            for idx, place in enumerate(state_info["Top 10 Must-Visit Places"]):
                with cols[idx % 3]:
                    st.image(place['image_url'], caption=place['name'], use_container_width=True)
        else:
            st.write("No information available for this state.")
    else:
        st.write("Please select a valid state.")
    # Display key metrics
    #st.subheader("State Information")
    st.subheader(f"Tourism Places Many more Available in {state} ")
    # Embed YouTube videos
    #st.subheader("YouTube Videos")
    #st.video("https://youtu.be/b0uVFvsbkDU?si=2rPi0J7CDiZYkA1w")  # Replace with actual video ID
    #st.video("https://youtu.be/Nntqx3oSGSA?si=kNZYOXTdBGzh9Heh")  # Replace with actual video ID


#Filter 2
elif dropdown_option == "Top Affordable Hotels":
    st.subheader(f"Top Affordable Hotels in {state}")
    st.write("👈 Filter Your Favorite States in the Sidebar")
    
    # Always show hotel information
    hotel_info = india_Hotel_info.get(state, india_Hotel_info["Andhra Pradesh"])  # Fallback to Andhra Pradesh if state not found
    
    cols = st.columns(3)  # Create 3 columns for hotel display
    for idx, hotel in enumerate(hotel_info["Top Affordable Hotels"]):
        with cols[idx % 3]:  # Cycle through columns
            st.image(hotel['image_url'], caption=hotel['hotel_name'], use_container_width=True)

#Filter 3

elif dropdown_option.startswith("Tourism Metrics"):
    st.write("👈 Filter Your Favorite States Side Bar")
    col1, col2, col3 = st.columns(3)
    col1.metric("Foreign Tourist Arrivals (Millions)", f"{filtered_df['FOREIGN_TOURIST_ARRIVALS_MILLIONS'].values[0]:,.2f}")
    col2.metric("Domestic Tourist Visits (Millions)", f"{filtered_df['DOMESTIC_TOURIST_VISITS_MILLIONS'].values[0]:,.2f}")
    col3.metric("Total Visitors (Millions)", f"{filtered_df['TOTAL_VISITORS_MILLIONS'].values[0]:,.2f}")
    col4, col5 = st.columns(2)
    
    with col4:
        st.subheader("📈 Annual Growth Rates")
        growth_data = {
            "Foreign": filtered_df["ANNUAL_GROWTH_RATE_FOREIGN"].values[0],
            "Domestic": filtered_df["ANNUAL_GROWTH_RATE_DOMESTIC"].values[0],
            "Total": filtered_df["ANNUAL_GROWTH_RATE_TOTAL"].values[0]
        }
        fig1, ax1 = plt.subplots()
        sns.barplot(x=list(growth_data.keys()), y=list(growth_data.values()), ax=ax1, palette="viridis")
        ax1.set_ylabel("Growth Rate (%)")
        ax1.set_title("Annual Growth Rates")
        for i, v in enumerate(growth_data.values()):
            ax1.text(i, v + 0.5, f"{v:.2f}%", ha='center')
        st.pyplot(fig1)
    
    with col5:
        st.subheader(f"📊 Year-over-Year Visitor Trends for **{state}**")
    
        state_data = df[df["STATE_UT"] == state].sort_values("YEAR")
    
        fig2, ax2 = plt.subplots(figsize=(10, 6))
    
        # Plot lines with different colors
        ax2.plot(
            state_data["YEAR"],
            state_data["FOREIGN_TOURIST_ARRIVALS_MILLIONS"],
            label="🌐 Foreign Visitors",
            marker='o',
            color=color_palette[0],
            linewidth=2.5
        )
        ax2.plot(
            state_data["YEAR"],
            state_data["DOMESTIC_TOURIST_VISITS_MILLIONS"],
            label="🏠 Domestic Visitors",
            marker='o',
            color=color_palette[1],
            linewidth=2.5
        )
        ax2.plot(
            state_data["YEAR"],
            state_data["TOTAL_VISITORS_MILLIONS"],
            label="👥 Total Visitors",
            marker='o',
            color=color_palette[2],
            linewidth=2.5
        )
    
        # Axis and title styling
        ax2.set_xlabel("Year", fontsize=12)
        ax2.set_ylabel("Visitors (Millions)", fontsize=12)
        ax2.set_title("📈 Visitor Trends Over the Years", fontsize=14, weight='bold')
        ax2.set_xticks(state_data["YEAR"])
        ax2.set_xticklabels(state_data["YEAR"], rotation=45, fontsize=10)
        ax2.tick_params(axis='y', labelsize=10)
        ax2.grid(True, linestyle='--', alpha=0.5)
    
        # Legend
        ax2.legend(loc="upper left", fontsize=10, frameon=True)
    
        # Display plot
        st.pyplot(fig2)
    
    # Second 2x2 grid for Popular Tourist Sites Word Cloud and Monument Visits by Region
    col6, col7 = st.columns(2)
    
    #Add Toursim sites
    with col6:
        st.subheader(f"🗺️ Highlighted Tourist Websites in **{state}**")
    
        # Randomly select 4 unique tourism sites
        random_sites = random.sample(tourism_sites, 4)
    
        # Define a list of nice colors
        color_palette = ["#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9", "#92A8D1", "#955251", "#B565A7", "#009B77"]
        random.shuffle(color_palette)
    
        # Create a blank figure
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.axis('off')
    
        # Display each site on a new line, centered with a random color
        for i, site in enumerate(random_sites):
            ax.text(
                0.5,                     # X position (centered)
                0.85 - i * 0.2,          # Y position spaced apart
                site,
                fontsize=22,
                ha='center',
                va='center',
                color=color_palette[i % len(color_palette)],  # Different color per line
                fontweight='bold',
                family='monospace',
                bbox=dict(facecolor='white', edgecolor='lightgray', boxstyle='round,pad=0.3')
            )
    
        st.pyplot(fig)   
    
    
    with col7:
        st.subheader("🏛️ Monument Visits by Region")
        region_data = df[df["YEAR"] == year].groupby("REGION")["MONUMENT_VISITS_MILLIONS"].sum().reset_index()
        fig4, ax4 = plt.subplots()
        sns.barplot(data=region_data, x="REGION", y="MONUMENT_VISITS_MILLIONS", ax=ax4, palette="magma")
        ax4.set_ylabel("Monument Visits (Millions)")
        ax4.set_title(f"Monument Visits by Region in {year}")
        for i, v in enumerate(region_data["MONUMENT_VISITS_MILLIONS"]):
            ax4.text(i, v + 0.1, f"{v:.2f}", ha='center')
        st.pyplot(fig4)
    
    # Third 2x2 grid for Tourism Revenue vs. Total Visitors and Correlation Heatmap
    col8, col9 = st.columns(2)
    
    with col8:
        st.subheader("💰 Tourism Revenue vs. Total Visitors")
        year_data = df[df["YEAR"] == year]
        fig5, ax5 = plt.subplots()
        sns.scatterplot(data=year_data, x="TOTAL_VISITORS_MILLIONS", y="TOURISM_REVENUE_CRORES", hue="REGION", ax=ax5, palette="Set2", s=100)
        ax5.set_xlabel("Total Visitors (Millions)")
        ax5.set_ylabel("Tourism Revenue (Crores)")
        ax5.set_title(f"Tourism Revenue vs. Total Visitors in {year}")
        st.pyplot(fig5)
    
    with col9:
        st.subheader("🔍 Correlation Tourism Metrics")
        metrics = ["FOREIGN_TOURIST_ARRIVALS_MILLIONS", "DOMESTIC_TOURIST_VISITS_MILLIONS", "TOTAL_VISITORS_MILLIONS", "TOURISM_REVENUE_CRORES", "MONUMENT_VISITS_MILLIONS"]
        corr = df[metrics].corr()
        fig6, ax6 = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax6)
        ax6.set_title("Correlation Heatmap")
        st.pyplot(fig6)


# Display Tourism Metrics header

    #col1, col2, col3 = st.columns(3)
    #col1.metric("Foreign Tourist Arrivals (Millions)", f"{filtered_df['FOREIGN_TOURIST_ARRIVALS_MILLIONS'].values[0]:,.2f}")
    #col2.metric("Domestic Tourist Visits (Millions)", f"{filtered_df['DOMESTIC_TOURIST_VISITS_MILLIONS'].values[0]:,.2f}")
    #col3.metric("Total Visitors (Millions)", f"{filtered_df['TOTAL_VISITORS_MILLIONS'].values[0]:,.2f}")

# Show images in a responsive 3x3 grid


# Create the first 2x2 grid for Annual Growth Rates and Visitor Trends


# Hide the map view initially
map_visible = False

# Create Plotly Choropleth map
fig = go.Figure(go.Choroplethmapbox(
    geojson=geojson,
    locations=states,
    z=[1] * len(states),
    featureidkey="properties.NAME_1",
    colorscale="Viridis",
    showscale=False,
    marker_opacity=0.5,
    marker_line_width=0.5
))

# Set map boundaries to focus on India
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=4,
    mapbox_center={"lat": 22.9734, "lon": 78.6569},
    mapbox_bounds={"west": 68.7, "south": 8.1, "east": 97.4, "north": 37.1},
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    clickmode='event+select'
)

# State Information Section

#st.markdown("### Click on a state in the map to see the welcome message.")

# Show images in a responsive 3x3 grid


st.markdown("<br>", unsafe_allow_html=True)

# Display the map below the images
if map_visible:
    st.plotly_chart(fig, use_container_width=True)

#st.subheader("Thank You For Visiting")
#st.title("By TamilRock Stars")
# Subheader with light-colored shadow for black background
st.markdown(
    """
    <h2 style="
        color: #fff;
        background: transparent;
        font-family: 'Segoe UI', sans-serif;
        text-align: center;
        letter-spacing: 2px;
        font-weight: 700;
        margin-bottom: 32px;
        font-size: 2.2em;
    ">
        Thank You For Visiting
    </h2>
    """,
    unsafe_allow_html=True
)

# "By TamilRock Stars" with neon multi-shadow effect
st.markdown(
    """
    <h1 style="
        color: #fff;
        background: transparent;
        font-family: 'Segoe UI', sans-serif;
        text-align: center;
        font-size: 2.5em;
        font-weight: 900;
        letter-spacing: 3px;
        margin-bottom: 0;
        text-shadow:
            0 0 8px #00fff7,
            0 0 16px #f633ff,
            0 0 24px #1e90ff,
            0 0 32px #00fff7,
            0 0 40px #f633ff;
    ">
        By TamilRock Stars
    </h1>
    """,
    unsafe_allow_html=True
)