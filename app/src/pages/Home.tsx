import * as React from "react";
import WordCloud, { OptionsProp, CallbacksProp, Word } from "react-wordcloud";
import moment, { Moment } from "moment";
import axios from "axios";
import prettyBytes from "pretty-bytes";
import { useHistory, Link } from "react-router-dom";
import DateRangePicker from '../components/DateRangerPicker'
import { useQuery } from "../hooks/query";
import { env } from "process";

const DATE_MOMENT_FORMAT = 'YYYYMMDD'

const words = [
  {
    text: "영화",
    value: 64,
  },
  {
    text: "관람객",
    value: 11,
  },
  {
    text: "너무",
    value: 16,
  },
  {
    text: "정말",
    value: 17,
  },
  {
    text: "correct",
    value: 10,
  },
  {
    text: "day",
    value: 54,
  },
  {
    text: "prescription",
    value: 12,
  },
  {
    text: "time",
    value: 77,
  },
  {
    text: "thing",
    value: 45,
  },
  {
    text: "left",
    value: 19,
  },
  {
    text: "pay",
    value: 13,
  },
  {
    text: "people",
    value: 32,
  },
  {
    text: "month",
    value: 22,
  },
  {
    text: "again",
    value: 35,
  },
  {
    text: "review",
    value: 24,
  },
  {
    text: "call",
    value: 38,
  },
  {
    text: "doctor",
    value: 70,
  },
  {
    text: "asked",
    value: 26,
  },
  {
    text: "finally",
    value: 14,
  },
  {
    text: "insurance",
    value: 29,
  },
  {
    text: "week",
    value: 41,
  },
  {
    text: "called",
    value: 49,
  },
  {
    text: "problem",
    value: 20,
  },
  {
    text: "going",
    value: 59,
  },
  {
    text: "help",
    value: 49,
  },
  {
    text: "felt",
    value: 45,
  },
  {
    text: "discomfort",
    value: 11,
  },
  {
    text: "lower",
    value: 22,
  },
  {
    text: "severe",
    value: 12,
  },
  {
    text: "free",
    value: 38,
  },
  {
    text: "better",
    value: 54,
  },
  {
    text: "muscle",
    value: 14,
  },
  {
    text: "neck",
    value: 41,
  },
  {
    text: "root",
    value: 24,
  },
  {
    text: "adjustment",
    value: 16,
  },
  {
    text: "therapy",
    value: 29,
  },
  {
    text: "injury",
    value: 20,
  },
  {
    text: "excruciating",
    value: 10,
  },
  {
    text: "chronic",
    value: 13,
  },
  {
    text: "chiropractor",
    value: 35,
  },
  {
    text: "treatment",
    value: 59,
  },
  {
    text: "tooth",
    value: 32,
  },
  {
    text: "chiropractic",
    value: 17,
  },
  {
    text: "dr",
    value: 77,
  },
  {
    text: "relief",
    value: 19,
  },
  {
    text: "shoulder",
    value: 26,
  },
  {
    text: "nurse",
    value: 17,
  },
  {
    text: "room",
    value: 22,
  },
  {
    text: "hour",
    value: 35,
  },
  {
    text: "wait",
    value: 38,
  },
  {
    text: "hospital",
    value: 11,
  },
  {
    text: "eye",
    value: 13,
  },
  {
    text: "test",
    value: 10,
  },
  {
    text: "appointment",
    value: 49,
  },
  {
    text: "medical",
    value: 19,
  },
  {
    text: "question",
    value: 20,
  },
  {
    text: "office",
    value: 64,
  },
  {
    text: "care",
    value: 54,
  },
  {
    text: "minute",
    value: 29,
  },
  {
    text: "waiting",
    value: 16,
  },
  {
    text: "patient",
    value: 59,
  },
  {
    text: "health",
    value: 49,
  },
  {
    text: "alternative",
    value: 24,
  },
  {
    text: "holistic",
    value: 19,
  },
  {
    text: "traditional",
    value: 20,
  },
  {
    text: "symptom",
    value: 29,
  },
  {
    text: "internal",
    value: 17,
  },
  {
    text: "prescribed",
    value: 26,
  },
  {
    text: "acupuncturist",
    value: 16,
  },
  {
    text: "pain",
    value: 64,
  },
  {
    text: "integrative",
    value: 10,
  },
  {
    text: "herb",
    value: 13,
  },
  {
    text: "sport",
    value: 22,
  },
  {
    text: "physician",
    value: 41,
  },
  {
    text: "herbal",
    value: 11,
  },
  {
    text: "eastern",
    value: 12,
  },
  {
    text: "chinese",
    value: 32,
  },
  {
    text: "acupuncture",
    value: 45,
  },
  {
    text: "prescribe",
    value: 14,
  },
  {
    text: "medication",
    value: 38,
  },
  {
    text: "western",
    value: 35,
  },
  {
    text: "sure",
    value: 38,
  },
  {
    text: "work",
    value: 64,
  },
  {
    text: "smile",
    value: 17,
  },
  {
    text: "teeth",
    value: 26,
  },
  {
    text: "pair",
    value: 11,
  },
  {
    text: "wanted",
    value: 20,
  },
  {
    text: "frame",
    value: 13,
  },
  {
    text: "lasik",
    value: 10,
  },
  {
    text: "amazing",
    value: 41,
  },
  {
    text: "fit",
    value: 14,
  },
  {
    text: "happy",
    value: 22,
  },
  {
    text: "feel",
    value: 49,
  },
  {
    text: "glasse",
    value: 19,
  },
  {
    text: "vision",
    value: 12,
  },
  {
    text: "pressure",
    value: 16,
  },
  {
    text: "find",
    value: 29,
  },
  {
    text: "experience",
    value: 59,
  },
  {
    text: "year",
    value: 70,
  },
  {
    text: "massage",
    value: 35,
  },
  {
    text: "best",
    value: 54,
  },
  {
    text: "mouth",
    value: 20,
  },
  {
    text: "staff",
    value: 64,
  },
  {
    text: "gum",
    value: 10,
  },
  {
    text: "chair",
    value: 12,
  },
  {
    text: "ray",
    value: 22,
  },
  {
    text: "dentistry",
    value: 11,
  },
  {
    text: "canal",
    value: 13,
  },
  {
    text: "procedure",
    value: 32,
  },
  {
    text: "filling",
    value: 26,
  },
  {
    text: "gentle",
    value: 19,
  },
  {
    text: "cavity",
    value: 17,
  },
  {
    text: "crown",
    value: 14,
  },
  {
    text: "cleaning",
    value: 38,
  },
  {
    text: "hygienist",
    value: 24,
  },
  {
    text: "dental",
    value: 59,
  },
  {
    text: "charge",
    value: 24,
  },
  {
    text: "cost",
    value: 29,
  },
  {
    text: "charged",
    value: 13,
  },
  {
    text: "spent",
    value: 17,
  },
  {
    text: "paying",
    value: 14,
  },
  {
    text: "pocket",
    value: 12,
  },
  {
    text: "dollar",
    value: 11,
  },
  {
    text: "business",
    value: 32,
  },
  {
    text: "refund",
    value: 10,
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

const message = (start: Moment, end: Moment) => {
  if (start.diff(end, "month") <= 1) {
    return `${end.year()}년 ${end.month()}월엔 대한민국에 어떤 일이 있었나요?`;
  }

  return `${start.year()}년 ${start.month()}월과 ${end.year()}년 ${end.month()}월엔 대한민국에 어떤 일이 있었나요?`;
};

function App() {
  const query = useQuery();
  const history = useHistory();
  const [page, setPage] = React.useState({
    loaded: false,
    min: null,
    max: null,
    dataSize: 0,
  });

  const [start, setStart] = React.useState<Moment>(
    query.get("start")
      ? moment(query.get("start"))
      : moment().subtract(1, "m")
  );
  const [end, setEnd] = React.useState<Moment>(
    query.get("end")
      ? moment(query.get("end"))
      : moment().subtract(1, "d")
  );

  const [section, setSection] = React.useState("it");

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
      if (word.lenght > 0) {
        window.location.href = `https://search.naver.com/search.naver?query=${encodeURIComponent(word.text)}&nso=${encodeURIComponent(`p:from${start.format(DATE_MOMENT_FORMAT)}to${end.format(DATE_MOMENT_FORMAT)}`)}`
      }
    }
  }

  // do not re-render when start and end are changed
  React.useEffect(() => {
    if (start && start.isAfter(end)) {
      history.push("/");
    }
    async function loadPage() {
      const { data } = await axios.get("api.krwordcloud.com/trend");
      setPage({
        loaded: true,
        min: data.minDate,
        max: data.maxDate,
        dataSize: data.dataSize,
      });
    }

    // loadPage();
  }, [start, end, history]);

  if (false && !page.loaded) {
    return <h1>Loading...</h1>;
  }

  return (
    <div className={"container"}>
      <header></header>
      <main className={"main"}>
        <div className={"message"}>
          <h1>{message(start, end)}</h1>
          <h4>{prettyBytes(192311092841984)}의 데이터를 분석하였습니다.</h4>
        </div>
        <div className="">
          <select onBlur={(e) => setSection(e.target.value)}>
            <option value="all">all</option>
            <option value="it">it</option>
            <option value="social">social</option>
            <option value="economy">economy</option>
            <option value="culture">culture</option>
          </select>
          {/* <DateRangePicker
            startDate={start}
            endDate={end}
            onDatesChange={({ startDate, endDate }): void => {
              if (startDate !== null && start !== startDate) {
                setStart(startDate);
              }
              if (endDate !== null && end !== endDate) {
                setEnd(end);
              }
            }}
          /> */}
          <DateRangePicker 
            startDate={start}
            endDate={end}
            onDatesChange={({ startDate, endDate }): void => {
              if (startDate !== null && start !== startDate) {
                setStart(startDate);
              }
              if (endDate !== null && end !== endDate) {
                setEnd(end);
              }
            }}
          />
          <Link
            to={`/wordcloud?start=${start.year()}-${start.month()}&end=${end.year()}-${end.month()}&section=${section}`}
          >
            <button type="button" className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
              Update
            </button>
          </Link>
        </div>
        <div className="">
          <WordCloud words={words} options={options} callbacks={callbacks} />
        </div>
      </main>
      <footer className=""></footer>
    </div>
  );
}

export default App;
