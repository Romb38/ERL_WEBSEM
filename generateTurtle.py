import csv
import uuid

dcterms = "@prefix dcterms: <http://purl.org/dc/terms/> ."
foaf = "@prefix foaf:  <http://xmlns.com/foaf/0.1/> ."
abo = "@prefix abo:   <http://artemisBookstore.com/ontology#> ."
rdfs = "@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> ."
xsd = "@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> ."

def generate_turtle(csv_file_name, text_file_name):
    with open(csv_file_name, mode='r', encoding='utf-8') as csv_file, \
         open(text_file_name, mode='w', encoding='utf-8') as text_file:

        text_file.write(dcterms + "\n")
        text_file.write(foaf + "\n")
        text_file.write(abo + "\n")
        text_file.write(rdfs + "\n")
        text_file.write(xsd + "\n\n")

        csv_reader = csv.reader(csv_file, delimiter=';')
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            author_family_name = row[0]
            author_given_name = row[1]
            book_title = row[2]
            pages_nb = int(row[3])
            isbn = row[4]
            publisher_name = row[5]

            id_writer = uuid.uuid5(uuid.NAMESPACE_DNS, author_family_name + "-" + author_given_name)
            id_publisher = uuid.uuid4()
            id_book = uuid.uuid5(uuid.NAMESPACE_DNS, isbn)

            output_line = f"""
abr:{id_writer} a abo:Writer;
    foaf:givenName "{author_given_name}" ;
    foaf:familyName "{author_family_name}" ;
    foaf:name "{author_given_name} {author_family_name}" .

abr:{id_publisher} a abo:Publisher;
    foaf:name "{publisher_name}" .

abr:{id_book} a abo:Book ;
    dcterms:title "{book_title}" ;
    abo:author abr:{id_writer} ;
    abo:isbn "{isbn}" ;
    abo:pages {pages_nb} ;
    dcterms:publisher abr:{id_publisher} .

"""
            text_file.write(output_line)

if __name__ == "__main__":
    try:
        generate_turtle("data/artemisBookstoreData-v1.csv", "data/generated/artemisBookstoreData-v1-en.txt")
        print("\nText data has been generated")
    except IOError as e:
        print("I/O Error while Generating Text Data")
        print(e)
