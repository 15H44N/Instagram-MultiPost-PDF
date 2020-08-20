im_path = './Images/'

import instaloader
from PIL import Image
import requests
import os
from fpdf import FPDF

def createPDFfromPost(scode,pdf_name):

    L = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(L.context, 
                                        shortcode= scode)

    post_img_urls = []
    if post.typename == 'GraphSidecar':
        for member in post.get_sidecar_nodes():
            if not member.is_video:
                post_img_urls.append(member.display_url)
                
    for idx,url in enumerate(post_img_urls):
        img = Image.open(requests.get(url, stream = True).raw)
        img.save("./Images/{}.jpg".format(str(idx)))

    pdf = FPDF()
    sdir = im_path
    w,h = 0,0
    for idx, filename in enumerate(sorted(os.listdir(im_path))) :
        fname = sdir + filename
        if os.path.exists(fname):
            if idx == 0:
                cover = Image.open(fname)
                w,h = cover.size
                pdf = FPDF(unit = "pt", format = [w,h])
            image = fname
            pdf.add_page()
            pdf.image(image,0,0,w,h)

    pdf.output("./{}.pdf".format(pdf_name), "F")
    return "{}.pdf".format(pdf_name)

def createPDFandRemove(v_dict):
    scode = v_dict.get('scode')
    fname = v_dict.get('fname')
    ret_val = createPDFfromPost(scode,fname)
    
    for filename in os.listdir(im_path):
        os.remove(im_path+filename)
    
    return ret_val