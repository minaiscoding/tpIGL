import os
import requests
#--------------------------------------------------------------------------------------------------------------
from .utils import (
    extract_pdf_metadata,
    generate_metadata_dict,
    extract_text_from_pdf,
    extract_information,
    analyze_texte,
    is_valid_scientific_pdf,
    is_valid_external_url,
    is_valid_localfilepath,
    download_pdf_from_url,
    validate_articleSci_pdf,
)
#--------------------------------------------------------------------------------------------------------------
from django.core.files.base import ContentFile
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
#--------------------------------------------------------------------------------------------------------------
from rest_framework.decorators import api_view
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
#--------------------------------------------------------------------------------------------------------------
from backendapp.models import Articles
from backendapp.serializers import  ArticlesSerializer
#--------------------------------------------------------------------------------------------------------------
from django.shortcuts import render
#--------------------------------------------------------------------------------------------------------------



#--------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------

                                   #**************************#
                                   #     GestionArticles      #
                                   #**************************#

#////////////////
# upload article
#////////////////

#///////////////////////////////////////////////////////////////////
'''
Lancer une opération d Upload des articles scientifiques à partir d une adresse URL contenant un ensemble 
d articles en format PDF, ces articles peuvent être en une colonne ou deux colonnes maximum. Le système 
récupère les fichiers PDF, il extrait le texte, il analyse ces textes pour extraire les informations caractérisant 
l article scientifique. Les informations extraites sont envoyées dans un index de recherche dans ElasticSearch.
'''
#///////////////////////////////////////////////////////////////////

#----------------------------------------------------------------------------------------------------
#  for testing
#*****************************************************************************  

def pdf_text_view(request):
    file_path = "C:\\Users\\dell\\Downloads\\Artificial_Intelligence_Enabled_Radio_Propagation_for_CommunicationsPart_I_Channel_Characterization_and_Antenna-Channel_Optimization.pdf"
    text = extract_text_from_pdf(file_path)
    return render(request, 'pdf_text.html', {'text': text})

#*****************************************************************************
def analize_text_view(request):
    
    file_path = "C:\\Users\\dell\\Downloads\\Artificial_Intelligence_Enabled_Radio_Propagation_for_CommunicationsPart_I_Channel_Characterization_and_Antenna-Channel_Optimization.pdf"

    # Extract text from the PDF file
    pdf_text = extract_text_from_pdf(file_path)

    # Analyze the extracted text
    #result = extract_information(pdf_text)
    metadata = extract_pdf_metadata(file_path)
    result = analyze_texte(pdf_text,metadata)

    # Render the template with the extracted information
    return render(request, 'ana_text.html', {'result': result})
#*****************************************************************************
def pdf_metadata_view(request):
    # Extract metadata from the PDF file
    pdf_path = "C:\\Users\\dell\\Downloads\\Artificial_Intelligence_Enabled_Radio_Propagation_for_CommunicationsPart_I_Channel_Characterization_and_Antenna-Channel_Optimization.pdf"
    metadata = extract_pdf_metadata(pdf_path)

    # Generate metadata dictionary
    metadata_dict = generate_metadata_dict(metadata)

    # Pass the metadata dictionary to the template
    return render(request, 'pdf_metadata_template.html', {'result': metadata_dict})


#*****************************************************************************
# to be tested by the end 
class UploadArticleView(APIView):
    parser_classes = (FileUploadParser, MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # Retrieve the URL from the request data
        url = request.data.get('url')
        # If the URL points to a directory, download PDFs from the directory
        articles_data = download_pdf_from_url(url)

        if articles_data:
            for article_data in articles_data:
                # Save only the URL in the 'url' field
                url_field_data = {'url': url}
                article_data.update(url_field_data)

                # Serialize the data and create an Article instance
                serializer = ArticlesSerializer(data=article_data)

                if serializer.is_valid():
                    article = serializer.save()

                    # Extraire le texte du PDF et analyser les informations
                    pdf_text = extract_text_from_pdf(article.pdf_file.path)
                    analysis_result = analyze_texte(pdf_text)

        

                    article.save()

            return Response({'message': 'Upload réussi'}, status=status.HTTP_201_CREATED)

        return Response({'error': 'Échec du téléchargement des PDFs depuis l\'URL'}, status=status.HTTP_400_BAD_REQUEST)

#///////////////////////////////////////////////////////////////////
# other version to review 
'''
class UploadArticleView(APIView):
     parser_classes = (MultiPartParser, FormParser)
     def post(self, request, *args, **kwargs):

        serializer = ArticlesSerializer(data=request.data)
        if serializer.is_valid():
           # Enregistrez le fichier PDF dans la base de données
           article = serializer.save()
           # Extract information from the uploaded PDF
           pdf_text = extract_text_from_pdf(article.pdf_file.path)

            # Analyser le texte et extraire les informations nécessaires
            # Vous devez implémenter la logique d'analyse en fonction de vos besoins
           return Response({'message': 'Upload réussi'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
           article_data = {
                    'Titre': ,
                    'Resume': ,
                    'auteurs': ,
                    'Institution': ,
                    'date': ,
                    'MotsCles': ,
                    'text': ,
                    'URL_Pdf': ,
                    'RefBib': ,
                }
           # Create a new article instance with the extracted information
           Articles.objects.create(**article_data)
           '''
'''
#--------------------------------------------------------------

'''
'''
def extract_text_from_file(article_file:str) -> [str]:
    with open(article_file,'rb') as pdf:
        reader = PyPDF2.PdfFileReader(pdf,strict=False)
        pdf_text = []

        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)
    

class UploadArticleView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ArticlesSerializer(data=request.data)

        if serializer.is_valid():
            # Extract information from the uploaded PDF
            article_file = request.FILES['article_file']

            try:
                # Open the PDF file using PyMuPDF
                pdf_document = fitz.open(article_file)
                
                # Assuming you want to extract text from the first page
                first_page = pdf_document[0]
                extracted_text = first_page.get_text("text")

                # Extracted information from the PDF

                # Modify this part based on your actual extraction logic
                extracted_title = "Title from PDF"
                extracted_resume = "Resume from PDF"
                extracted_authors = "Authors from PDF"
                extracted_institution = "Institution from PDF"
                extracted_date = "Date from PDF"
                extracted_mots_cles = "MotsCles from PDF"
                extracted_text = first_page.get_text("text")
                extracted_url_pdf = "URL_Pdf from PDF"
                extracted_ref_bib = "RefBib from PDF"

                # Create a new article instance with the extracted information
                article_data = {
                    'Titre': extracted_title,
                    'Resume': extracted_resume,
                    'auteurs': extracted_authors,
                    'Institution': extracted_institution,
                    'date': extracted_date,
                    'MotsCles': extracted_mots_cles,
                    'text': extracted_text,
                    'URL_Pdf': extracted_url_pdf,
                    'RefBib': extracted_ref_bib,
                }

                Articles.objects.create(**article_data)

                return Response({'message': 'Article uploaded and information extracted.'}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            finally:
                pdf_document.close()

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



'''









#///////////////////////

#///////////////////////

def scientific_pdf_view(request):
    # Call the test_scientific_pdf function to get the validation result
    url='C:\\Users\\dell\\Downloads\\ScienceDirect_articles_14Dec2023_23-22-46.478\\An-Introduction-to-Machine-Learning--a-per_2023_Physica-A--Statistical-Mecha.pdf'
    url2='C:\\Users\\dell\\Downloads\\Artificial_Intelligence_Enabled_Radio_Propagation_for_CommunicationsPart_I_Channel_Characterization_and_Antenna-Channel_Optimization.pdf'
    is_valid = validate_articleSci_pdf(url2)

    # Prepare the context data to pass to the template
    context = {'is_valid': is_valid}

    # Render the template with the context data
    return render(request, 'test_scientific_pdf.html', context)

