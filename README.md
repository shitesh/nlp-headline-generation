# nlp-topic-detection

repo for nlp project - Automated natural language headline generation using learning models

**INTRODUCTION:**<br/>
Headline generation is an important problem in Text Summarization and has several practical applications. The headline of a text, especially a news article is a compact, grammatical and coherent representation of important pieces of information in the news article. Although newspaper articles are usually accompanied by headlines, there are numerous other types of news text sources, such as transcripts of radio and television broadcasts and machine translated texts where such summary information is missing. We plan to generate automatic natural language headline generation for Hindi language where no major work has been done yet.

**METHOD:**

**Data Sources:**<br/>
	1. HindMonoCorp, a monolingual corpus of Hindi. HindMonoCorp amounts to 87 million tokens in 44 million sentences.  
	2. Hindi web texts (HWT), a monolingual corpus containing Hindi news articles.  
	3. Google news(Hindi) - If needed, we will crawl Google news to extract group of headlines and  news stories    
	4. Hindi Wordnet -  used for evaluating the performance.  
**POS Tagger**<br/>
							Python NLTK tool and Siva Reddy’s Hindi Part of speech tagger.  

**Procedure:**  
The entire process can be divided in following steps:  
	1. Pre-processing Step: Tokenization and removal of special characters, POS.           
	2. Headline Generation:  
		a)  Content selection: This step assigns each word in the news story a probability of its inclusion in the headline.  
		b) Headline synthesis: This step assigns a score to the sequence of surface word ordering of a particular headline candidate by modeling the probability of headline word sequences in the context of the news story.   
		c)Decoding: In  this step, we use a decoding algorithm which explores the space of candidate headline hypothesis to generate optimal headline word sequence.  
 	3. Post-processing: Fixing verb tense of the headline.  

We will use maximum entropy models for Content Selection and Headline Synthesis. For decoding, a beam search algorithm is used that combines the two models to produce a list of k-best headlines for a news story.  

**Evaluation:**  

For evaluating, we will use a combination of cosine similarity and word order similarity to compare the generated headlines with actual headlines.  
Similarity between two sentences T1 and T2 will be calculated as   
        S(T1, T2) = SS(T1, T2) + (1- )SR(T1,T2)[1]   
where SR is word order similarity and is given by SR= 1-[(r1-r2)/(r1+r2)]  
and SS is cosine similarity and is given by SS =(s1*s2)/(|s1| .|s2| )   
This will cover both the semantic and syntactic information of the sentences.[1]   
 
**REFERENCES:**  
 	1. (https://pdfs.semanticscholar.org/5b43/d3ffbc8b1d0bd3e1b5c1322fb31254bcd0ad.pdf)  
 	2. (https://bitbucket.org/sivareddyg/hindi-part-of-speech-tagger)  
 	3. (https://www.cs.sfu.ca/~anoop/students/agattani/agattani_ msc_project.pdf)  



