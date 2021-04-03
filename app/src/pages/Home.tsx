import * as React from "react";
import WordCloud, { OptionsProp, CallbacksProp, Word } from "react-wordcloud";
import moment from "moment";
import axios from "axios";
import qs from 'qs'
import { useHistory } from "react-router-dom";
import ControlPanel, { Category } from '../components/ControlPanel';
import Message from '../components/Message'
import { useQuery } from "../hooks/query";
import { createImportSpecifier } from "typescript";

const loadingWords = [
  {
    text: "Loading",
    value: 5000,
  },
];

const calcFontSize = (width: number): [number, number] => {
  if (width < 576) {
    return [10, 60];
  }

  if (width >= 576) {
    return [12, 80];
  }

  if (width >= 768) {
    return [14, 100];
  }

  if (width >= 992) {
    return [18, 120];
  }

  if (width >= 1200) {
    return [24, 200];
  }

  return [10, 60];
};

function App() {
  const query = useQuery();
  const history = useHistory();
  const [loaded, setLoaded] = React.useState<boolean>(false)
  const [stats, setStats] = React.useState<{
    minDate: Date|null,
    maxDate: Date|null,
    size: number,
    pressOptions: string[]
  }>({
    minDate: null,
    maxDate: null,
    size: 0,
    pressOptions: []
  });
  const [trend, setTrend] = React.useState<{
    size: number,
    words: Word[]
  }>({
    size: 0,
    words: []
  });

  const start = moment(query.get("start")).isValid() ? moment(query.get("start")) : moment().subtract(1, "M");
  const end = moment(query.get("end")).isValid() ? moment(query.get("end")) : moment().subtract(1, "d");
  const presses = (query.get("press")?.split(",").map((press) => press.trim())) || [];
  const categories = ((query.get("category")?.split(",").map((category) => category.trim())) || []) as (keyof typeof Category)[];

  const options: OptionsProp = {
    enableTooltip: true,
    deterministic: false,
    fontFamily: "Spoqa Han Sans Neo",
    fontSizes: calcFontSize(window.innerWidth),
    fontStyle: "normal",
    fontWeight: "normal",
    padding: 1,
    rotations: 0,
    rotationAngles: [0, 90],
    scale: "sqrt",
    spiral: "archimedean",
    transitionDuration: 1000,
  };

  const callbacks: CallbacksProp = {
    onWordClick: (word: Word, event?: MouseEvent) => {
      const NAVER_DATE_FORMAT = 'YYYYMMDD'
      if (loaded && word.text.length > 0) {
        const nso = `p:from${start.format(NAVER_DATE_FORMAT)}to${end.format(NAVER_DATE_FORMAT)}`
        window.location.href = `https://search.naver.com/search.naver?query=${encodeURIComponent(word.text)}&nso=${encodeURIComponent(nso)}`
      }
    }
  }

  React.useEffect(() => {
    async function loadPage() {
      let trendStatsUrl = `http://${process.env.API_HOST}:${process.env.API_PORT}/v1/trend/stats/latest`

      try {
        const { data } = await axios.get(trendStatsUrl);
        setStats({
          minDate: data.start,
          maxDate: data.end,
          size: data.size,
          pressOptions: data.presses,
        });
      } catch (e) {
        console.error(e)
        return
      }

      let trendReqUrl = `http://${process.env.API_HOST}:${process.env.API_PORT}/v1/trend`
      const queryObject: { [key: string]: string } = {}
      if (start) {
        queryObject.start = start.format("YYYY-MM-DD")
      }
      if (end) {
        queryObject.end = end.format("YYYY-MM-DD")
      }
      if (categories.length > 0) {
        queryObject.category = categories.join(',')
      }
      if (presses.length > 0) {
        queryObject.category = presses.join(',')
      }
      if (Object.keys(queryObject).length > 0) {
        trendReqUrl = `${trendReqUrl}?${qs.stringify(queryObject)}`
      }

      try {
        const { data } = await axios.get(trendReqUrl);
        setTrend({
          size: data.size,
          words: Object.entries(data.score).map(([key, value]) => ({text: key, value}) as Word),
        });
      } catch (e) {
        console.error(e)
        return
      }
      setLoaded(true)
    }

    loadPage();
  }, []);

  return (
    <div className="h-screen w-screen">
      <header></header>
      <main className="w-full h-full">
        <div className="w-full" style={{height: 100}}>
          <Message start={start} end={end} size={stats.size} />
        </div>
        <div className="fixed top-2 right-2">
          <ControlPanel
            defaultStart={start}
            defaultEnd={end}
            defaultCategories={categories}
            defaultPresses={presses}
            pressOptions={stats.pressOptions}
            minDate={stats.minDate && moment(stats.minDate).isValid() ? moment(stats.minDate) : moment('2010-01-01')}
            maxDate={stats.maxDate && moment(stats.maxDate).isValid() ? moment(stats.maxDate) : moment()}
          />
        </div>
        <div className="w-full" style={{height: "calc(100vh - 100px)"}}>
          <WordCloud
            words={loaded ? trend.words : loadingWords}
            options={options}
            callbacks={callbacks}
          />
        </div>
      </main>
      <footer className=""></footer>
    </div>
  );
}

export default App;
