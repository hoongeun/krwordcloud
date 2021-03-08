Airflow Version : 2.0.0
Hadoop Version : 3.2.2
Hive vesion : 3.1.2
	- user : hive, password : hive, host : localhost, port : 10000
	- Database : news
		- table : verify_table(news_date date, category varchar(20), hash_data string, file_size double)
			- delimiter : \t, escape : \\, null defined as 'null'
		- table : article_table(news_date date, category varchar(20), written_time string, times_name varchar(30), headline string, contents string, url string)
			- delimiter : \t, escape : \\, null defined as 'null'
			!!변경 필요 : column 구성 변경 - news_date date, category varchar(20), news_contents<written_time string, times_name varchar(30), headline string, contents string, url string>[Map]
				-> news_date와 category로 해당 news 데이터들을 묶기 위함.
				
기존 파일에 hash\_writer.py와 insert\_db.py 파일 추가 생성
파일이 저장되는 장소는 해당 폴더 내의 output파일

pyhive에 앞서 sasl을 설치해야 하지만 현재 python3에서 sasl을 설치하기 위해서는 다음 작업이 필요
- ubuntu 기준 libsasl2-dev libsasl2-2 libsasl2-modules-gssapi-mit 패키지 인스톨

현재 Crawler에 포함된 파일 기준 sportcrawler.py와 sample.py는 사용하지 않음.

Articlecrawler.py 내에서 다른 파일의 함수를 호출하는 변수 이름들
writer - Writer.py
inserter - Insert_db.py


실행 파일 : Articlecrawler.py
