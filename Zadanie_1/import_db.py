import json
import csv
import datetime


conversations = open("Zadanie_1/conversations.jsonl", "r")
authors =  open("Zadanie_1/authors.jsonl", "r")

class Writer:
    def __init__(self, name:str,  limit, header):
        self.name = name
        self.header = header
        self.limit = limit
        self.dict = {}
        self.filecounter = 1
        self.linecounter = 0
        self.file = open(f'Zadanie_1/{self.name}_{self.filecounter}.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file, delimiter=";", escapechar="%")
        self.writer.writerow(self.header)
    
    def write(self, payload, flag=False):
        self.writer.writerow(payload)
        if flag:
            self.dict[payload[0]] = "0" 
        self.linecounter+=1
        if self.linecounter >= self.limit:
            self.linecounter=0
            self.filecounter+=1
            self.file.close()
            
            self.file = open(f'Zadanie_1/{self.name}_{self.filecounter}.csv', 'w', newline='', encoding='utf-8')
            self.writer = csv.writer(self.file, delimiter=";", escapechar="%")
            self.writer.writerow(self.header)

authors_csv_writer = Writer("authors", 10000000, ["id", "name", "username" ,"description", "tweet_count", "followers_count", "following_count", "listed_count"])
conversation_csv_writer= Writer("conversations", 5000000, ["id", "author_id", "content" ,"possibly_sensitive", "language", "source", "retweet_count", "reply_count", "like_count", "quote_count", "created_at"])
domain_csv_writer= Writer("context_domains", 100, ["id", "name", "description"])
entity_csv_writer= Writer("context_entities", 30000, ["id", "name", "description"])
annotation_csv_writer= Writer("annotations",50000000, ["id", "conversation_id", "value", "type", "probability"])
link_csv_writer= Writer("links", 20000000, ["id", "conversation_id", "url", "title", "description"])
reference_csv_writer= Writer("conversation_references", 5000000, ["id", "conversation_id", "parent_id", "type"])
hashtag_csv_writer= Writer("hashtags",1000000, ["id", "tag"])
conversation_hashtag_csv_writer= Writer("conversation_hashtags", 10000000, ["id", "conversation_id", "hashtag_id"])
context_annotation_csv_writer= Writer("context_annotations", 15000000, ["id", "conversation_id", "context_domain_id", "context_entity_id"])


time_authors_file = open(f'Zadanie_1/time_authors.csv', 'w', newline='', encoding='utf-8')
time_csv_writer = csv.writer(time_authors_file, delimiter=";", escapechar="%")
time_csv_writer.writerow(["Number of rows", "time"])


author_dict = {}
i = 0
time = ""


time_authors_start = datetime.datetime.now().isoformat()
time_csv_writer.writerow([i, time_authors_start])

for author_line in authors:
    line = json.loads(author_line)

    author_dict = annotation_csv_writer.dict

    if line["id"] in author_dict:
        continue
    
    author_record = [line["id"]]
    
    if "name" in line and line["name"]!="":
        author_record.append(line["name"].encode('utf8').replace(b'\x00', b'\uFFFD').decode("utf8"))
    else:
        author_record.append(None)

    if "username" in line and line["username"]!="":
        author_record.append(line["username"].encode('utf8').replace(b'\x00', b'\uFFFD').decode("utf8"))
    else:
        author_record.append(None)

    if "description" in line and line["description"]!="":
        author_record.append(line["description"].encode('utf8').replace(b'\x00', b'\uFFFD').decode("utf8"))
    else:
        author_record.append(None)

    if "public_metrics" in line and line["public_metrics"]!="":
        if "tweet_count" in line["public_metrics"] and line["public_metrics"]["tweet_count"]!="":
            author_record.append(line["public_metrics"]["tweet_count"])
        else:
            author_record.append(None)
        
        if "followers_count" in line["public_metrics"]and line["public_metrics"]["followers_count"]!="":
            author_record.append(line["public_metrics"]["followers_count"])
        else:
            author_record.append(None)
        
        if "following_count" in line["public_metrics"]and line["public_metrics"]["following_count"]!="":
            author_record.append(line["public_metrics"]["following_count"])
        else:
            author_record.append(None)
        
        if "listed_count" in line["public_metrics"]and line["public_metrics"]["listed_count"]!="":
            author_record.append(line["public_metrics"]["listed_count"])
        else:
            author_record.append(None)
    else:
        author_record.extend([None,None,None,None])
    
    authors_csv_writer.write(author_record, True)

    if i%100000 == 0 and i!=0:
        time = datetime.datetime.now().isoformat()
        time_csv_writer.writerow([i, time])
        print(author_record)
    i+=1

time_authors_end = datetime.datetime.now().isoformat()
time_csv_writer.writerow([i, time_authors_end])
time_authors_file.close()

hash_dict = {}
domain_dict = {}
entity_dict = {}
convo_dict = {}
tag_id = 0
convo_hashtag_id = 0
annotations_id = 0
context_anot_id = 0
reference_id = 0
url_id = 0

i=0

time_conversations_file = open(f'Zadanie_1/time_conversations.csv', 'w', newline='', encoding='utf-8')
time_csv_writer = csv.writer(time_conversations_file, delimiter=";", escapechar="%")
time_csv_writer.writerow(["Number of rows", "time"])

time_conversations_start = datetime.datetime.now().isoformat()
time_csv_writer.writerow([i, time_conversations_start])

for convo_line in conversations:
    line = json.loads(convo_line)
    
    convo_dict = conversation_csv_writer.dict

    if line["id"] not in convo_dict:
            
        convo_record = [line["id"]]
        convo_record.append(line["author_id"])
        convo_record.append(line["text"].encode('utf8').replace(b'\x00', b'\uFFFD').decode("utf8"))
        convo_record.append(line["possibly_sensitive"])
        convo_record.append(line["lang"])
        convo_record.append(line["source"].encode('utf8').replace(b'\x00', b'\uFFFD').decode("utf8"))

        if "public_metrics" in line and line["public_metrics"]!="":
            if "retweet_count" in line["public_metrics"] and line["public_metrics"]["retweet_count"]!="":
                convo_record.append(line["public_metrics"]["retweet_count"])
            else:
                convo_record.append(None)
            
            if "reply_count" in line["public_metrics"]and line["public_metrics"]["reply_count"]!="":
                convo_record.append(line["public_metrics"]["reply_count"])
            else:
                convo_record.append(None)
            
            if "like_count" in line["public_metrics"]and line["public_metrics"]["like_count"]!="":
                convo_record.append(line["public_metrics"]["like_count"])
            else:
                convo_record.append(None)
            
            if "quote_count" in line["public_metrics"]and line["public_metrics"]["quote_count"]!="":
                convo_record.append(line["public_metrics"]["quote_count"])
            else:
                convo_record.append(None)
        
        else:
            convo_record.extend([None,None,None,None])

        convo_record.append(line["created_at"])

        conversation_csv_writer.write(convo_record, True)
        
        if line["author_id"] not in author_dict:
            author_dict[line["author_id"]]="0"
            author_record = [line["author_id"], None, None, None, None, None, None, None]
            authors_csv_writer.write(author_record)

        
        if "entities" in line:
            if "hashtags" in line["entities"]:
                for tag in line["entities"]["hashtags"]:
                    convo_tag_record = [convo_hashtag_id]
                    convo_hashtag_id +=1
                    if tag["tag"] in hash_dict:
                        convo_tag_record.extend([line["id"], hash_dict[tag["tag"]]])
                    else:
                        hash_dict[tag["tag"]] = tag_id
                        tag_record = [tag_id, tag["tag"]]
                        convo_tag_record.extend([line["id"], tag_id])
                        hashtag_csv_writer.write(tag_record)
                        tag_id+=1
                    
                    conversation_hashtag_csv_writer.write(convo_tag_record)
            
            if "annotations" in line["entities"]:
                for anot in line["entities"]["annotations"]:
                    if anot["normalized_text"]!='':
                        annotations_record = [annotations_id, line["id"], anot["normalized_text"], anot["type"], anot["probability"]]
                        annotation_csv_writer.write(annotations_record)
                        annotations_id+=1
            
            if "urls" in line["entities"]:
                for url in line["entities"]["urls"]:
                    if len(url["expanded_url"]) < 2048:
                        url_record = [url_id, line["id"], url["expanded_url"], None, None]
                        url_id+=1
                        if "title" in url:
                            url_record[3] = url["title"].encode('utf8').replace(b'\x00', b'\uFFFD').decode("utf8")
                        if "description" in url:
                            url_record[4] = url["description"].encode('utf8').replace(b'\x00', b'\uFFFD').decode("utf8")

                        link_csv_writer.write(url_record)


        if "context_annotations" in line:
            for cont_anot in line["context_annotations"]:
                cont_anot_record = [context_anot_id, line["id"], None, None]
                context_anot_id+=1
                if "domain" in cont_anot:
                    if cont_anot["domain"]["id"] in domain_dict:
                        pass
                    else:
                        domain_dict[cont_anot["domain"]["id"]] = "0"
                        domain_record = [cont_anot["domain"]["id"], cont_anot["domain"]["name"].encode('utf8').replace(b'\x00', b'\uFFFD').decode("utf8")]
                        if "description" in cont_anot["domain"]:
                            domain_record.append(cont_anot["domain"]["description"].encode('utf8').replace(b'\x00', b'\uFFFD').decode("utf8"))
                        else:
                            domain_record.append(None)
                        domain_csv_writer.write(domain_record)
                    cont_anot_record[2] = cont_anot["domain"]["id"]
                
                if "entity" in cont_anot:
                    if cont_anot["entity"]["id"] in entity_dict:
                        pass
                    else:
                        entity_dict[cont_anot["entity"]["id"]] = "0"
                        entity_record = [cont_anot["entity"]["id"], cont_anot["entity"]["name"].encode('utf8').replace(b'\x00', b'\uFFFD').decode("utf8")]
                        if "description" in cont_anot["entity"]:
                            entity_record.append(cont_anot["entity"]["description"].encode('utf8').replace(b'\x00', b'\uFFFD').decode("utf8"))
                        else:
                            entity_record.append(None)
                        entity_csv_writer.write(entity_record)
                    cont_anot_record[3] = cont_anot["entity"]["id"]
                
                context_annotation_csv_writer.write(cont_anot_record)

        if "referenced_tweets" in line:
            for ref in line["referenced_tweets"]:
                refer_record = [reference_id, line["id"], ref["id"], ref["type"]]
                reference_id+=1
                reference_csv_writer.write(refer_record)

        if i%100000 == 0 and i!=0:
            time = datetime.datetime.now().isoformat()
            time_csv_writer.writerow([i, time])
            print(convo_record)
        i+=1

time_conversations_end = datetime.datetime.now().isoformat()
time_csv_writer.writerow([i, time_conversations_end])
time_conversations_file.close()