import requests
from bs4 import BeautifulSoup
# 다음영화 - 예매순위 페이지(http://ticket2.movie.daum.net/Movie/MovieRankList.aspx)에서 영화별 상세페이지에 접속하여 영화의 제목 / 평점 / 장르 / 감독 / 배우 데이터를 수집
# 상영중 영화 페이지에 데이터를 요청
raw = requests.get("http://ticket2.movie.daum.net/Movie/MovieRankList.aspx",
                   headers={"User-Agent":"Mozilla/5.0"})
html = BeautifulSoup(raw.text, 'html.parser')

# 컨테이너 수집
movies = html.select("ul.list_boxthumb > li")

# 수집한 컨테이너(영화) 반복
for m in movies:

    # 제목 수집해서 링크 저장
    title = m.select_one("strong.tit_join > a")
    url = title.attrs["href"]

    # 상세페이지 데이터 요청
    raw_each = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    html_each = BeautifulSoup(raw_each.text, 'html.parser')

    # 데이터 수집 시도
    try:
        # 제목, 평점, 장르, 감독, 배우 수집
        title = html_each.select_one("strong.tit_movie").text
        score = html_each.select_one("em.emph_grade").text

        # dd 태그 안에 데이터를 순서로 구분
        genre = html_each.select_one("dl.list_movie > dd:nth-of-type(1)").text
        director = html_each.select("dl.list_movie > dd:nth-of-type(5) a")
        actor = html_each.select("dl.list_movie > dd:nth-of-type(6) a")

    # 데이터를 수집할 수 없는 경우(상세페이지가 없는 경우)/ 상세페이지가 없습니다를 출력
    except:
        print(title.text.strip(), "상세페이지가 없습니다.")
        print("="*50)
        continue

    print("제목:", title)
    print("평점:", score)
    print("장르:", genre)

    print("감독:")
    for d in director:
        print(d.text)

    print("배우:")
    for a in actor:
        print(a.text)

    print("="*50)