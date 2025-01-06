import os
import random
import time

from astrapy import DataAPIClient
from astrapy.constants import VectorMetric
from astrapy.info import CollectionVectorServiceOptions
from tqdm import tqdm

random.seed(time.time())
client = DataAPIClient(os.environ["ASTRA_DB_APPLICATION_TOKEN"])
db = client.get_database_by_api_endpoint(os.environ["ASTRA_DB_API_ENDPOINT"])

collection_name = os.environ['ASTRA_DB_COLLECTION_NAME']
created_collection_names = db.list_collection_names()

if collection_name not in created_collection_names:
    print("Collection does not exists. creating collection.")
    db.create_collection(collection_name, dimension=1024, metric=VectorMetric.COSINE,
                         service=CollectionVectorServiceOptions(provider="nvidia", model_name="NV-Embed-QA"))

collection = db.get_collection("social_media_engagement")

social_media_engagement_count = 1000
instagram_post_types = [
    "static image",
    "carousel",
    "video",
    "reels",
    "stories",
    "instagram live",
    "guides",
    "collaborative",
    "sponsored",
    "highlights"
]

cnt = 0
data = []
for i in tqdm(range(social_media_engagement_count)):
    if cnt >= 100:
        collection.insert_many(data)
        data = []
        cnt = 0
    instagram_post_type = random.choice(instagram_post_types)
    data.append({
        "likes": random.randint(5, 50000),
        "shares": random.randint(10, 10000),
        "comments": random.randint(5, 9000),
        "posttype": instagram_post_type,
        "$vectorize": instagram_post_type,
        "metadata": {"likes": random.randint(5, 50000), "shares": random.randint(10, 10000),
                     "comments": random.randint(5, 9000), "posttype": instagram_post_type}
    })
    cnt += 1

if data:
    collection.insert_many(data)

print("Data stored.")
