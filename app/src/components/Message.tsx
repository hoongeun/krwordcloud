import { Moment } from 'moment'
import prettyBytes from 'pretty-bytes'

export type MessageProps = {
    start: Moment,
    end: Moment,
    size: number,
}

const Message = ({ start, end, size }: MessageProps) => {
    const message = start.diff(end, "day") <= 1 ? `${end.year()}년 ${end.month()}월 ${end.date()}일엔 대한민국에 어떤 일이 있었나요?` : `${start.year()}년 ${start.month()}월 ${start.date()}일과 ${end.year()}년 ${end.month()}월 ${end.date()}일엔 대한민국에 어떤 일이 있었나요?`
    const description = `${prettyBytes(size)}의 데이터를 분석하였습니다.`
    return (
        <>
            <h1 className="text-4xl font-bold leading-7 text-gray-900 mt-3 text-center">{message}</h1>
            <h3 className="text-center">{description}</h3>
        </>
    )
}

export default Message