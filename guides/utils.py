import json
from django.urls import reverse
from web_app.utils import getAlumniOf, getExpertise
from bs4 import BeautifulSoup


def getReviewedBy(blog_obj, url_prefix):
    doctor_obj = blog_obj.reviewed_by
    doctor_url = url_prefix + reverse("web_app:doctor_url", args=[doctor_obj.slug])
    return [
        {
            "@type": "Person",
            "name": doctor_obj.name,
            "url": doctor_url,
            "honorificPrefix": doctor_obj.honorific_prefix,
            "honorificSuffix": doctor_obj.honorific_suffix,
            "description": doctor_obj.description,
            "knowsAbout": getExpertise(doctor_obj),
            "alumniOf": getAlumniOf(doctor_obj),
            "sameAs": list(doctor_obj.social_links.values_list("url",flat=True))
        }
    ]


def getAllImages(soup):
    img = soup.select("img")
    images = []
    for i in img:
        if i.get("src"):
            image_schema = {
                "@type": "ImageObject",
                "url": i["src"]
            }
            if i.get("alt"):
                image_schema["caption"] = i["alt"]
            if i.get("width"):
                image_schema["width"] = i["width"]  
            if i.get("height"):
                image_schema["height"] = i["height"]  
            images.append(image_schema)
    return images


def getAuthor(blog_obj, url_prefix):
    doctor_obj = blog_obj.created_by
    doctor_url = url_prefix + reverse("web_app:doctor_url", args=[doctor_obj.slug])
    return {
        "@type": "Person",
        "name": doctor_obj.name,
        "url": doctor_url,
        "description": doctor_obj.description,
        "knowsAbout": getExpertise(doctor_obj),
        "alumniOf": getAlumniOf(doctor_obj),
        "sameAs": list(doctor_obj.social_links.values_list("url",flat=True))
    }


def getPublisher(blog_obj):
    publisher_obj = blog_obj.publisher
    publisher_schema = {
        "@type": "Organization",
        "name": publisher_obj.name,
        "logo": publisher_obj.logo.url,
        "url": publisher_obj.orgUrl,
        "email": publisher_obj.mail,
        "address": "",
        "contactPoint": {},
        "address": {},
        "parentOrganization": {},
        "sameAs": [],
    }
    return None


def getAbout(blog_obj, url_prefix):
    soup = BeautifulSoup(blog_obj.content, 'html.parser')
    article_url = url_prefix + reverse("guides:blog_url", args=[blog_obj.url_slug])
    about_schema = {
        "@type": "MedicalWebPage",
        "url": article_url,
        "headline": blog_obj.meta_title,
        "description": blog_obj.meta_desc,
        "datePublished": blog_obj.created_at.isoformat(),
        "lastReviewed": blog_obj.reviewed_at.isoformat(),
        "dateModified": blog_obj.updated_at.isoformat(),
        "inLanguage": "en-US",
        "image": getAllImages(soup),
        "video": [],
        "author": getAuthor(blog_obj,url_prefix),
        "citation": [],
        "SubjectOf": [],
        "about": [],
        "mentions": []
    }
    # if blog_obj.publisher:
    #     about_schema["publisher"] = getPublisher(blog_obj),
    return about_schema



def generateWebPageSchema(blog_obj, url_prefix):
    person_schema_body = {
        "@context": "https://schema.org",
        "@type": [
            "WebPage"
        ]
    }
    
    person_schema_body["reviewedBy"] = getReviewedBy(blog_obj, url_prefix)
    person_schema_body["about"] = getAbout(blog_obj, url_prefix)

    person_schema = '<script type="application/ld+json">'
    person_schema += json.dumps(person_schema_body)
    person_schema += '</script>'
    return person_schema
