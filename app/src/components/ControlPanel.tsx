import React from 'react'
import moment, { Moment } from 'moment'
import Select from 'react-select'
import { Link } from 'react-router-dom';
import qs from 'qs'
import DateRangePicker from './DateRangerPicker'


type Categories = {
    value: 'it',
    label: 'IT'
} | {
    value: 'society',
    label: '사회'
} | {
    value: 'economy',
    label: '경제'
} | {
    value: 'culture',
    label: '문화/생활'
}

type OptionType = {
    value: string,
    label: string
}

export type ControlPanelProps = {
    defaultStart: Moment,
    defaultEnd: Moment,
    defaultCategories: Categories[]
    defaultPresses: string[]
    pressOptions: string[]
}

const ControlPanel = ({ defaultStart, defaultEnd, defaultCategories, defaultPresses, pressOptions }: ControlPanelProps) => {
    const [start, setStart] = React.useState<Moment>(moment(defaultStart));
    const [end, setEnd] = React.useState<Moment>(moment(defaultEnd));
    const [categories, setCategories] = React.useState<Categories[]>(defaultCategories)
    const [presses, setPresses] = React.useState<OptionType[]>(defaultPresses.map((p) => ({ value: p, label: p})))
    const queryString = qs.stringify({
        start: start.format('YYYYMMDD'),
        end: end.format('YYYYMMDD'),
        category: categories.map((c) => c.value),
        press: presses.map((p) => p.value)
    })
    return (
        <div className="bg-blue-100 px-6 py-6">
            <div className="my-2">
                <div className="">날짜 선택</div>
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
            </div>
            <div className="my-6">
                <div className="">카테고리</div>
                <Select
                    defaultValue={defaultCategories}
                    isMulti
                    options={[
                        {
                            value: 'it',
                            label: 'IT'
                        }, {
                            value: 'society',
                            label: '사회'
                        }, {
                            value: 'economy',
                            label: '경제'
                        }, {
                            value: 'culture',
                            label: '문화/생활'
                        }
                    ]}
                    isClearable
                    onChange={(value) => {
                        setCategories(value as Categories[])
                    }}
                />
                <div className="text-sm text-gray-600">미 선택 - 전체 카테고리</div>
            </div>
            <div className="my-2">
                <div className="">언론사</div>
                <Select
                    defaultValue={defaultPresses}
                    isMulti
                    options={pressOptions.map((p) => ({ value: p, label: p }))}
                    onChange={(value) => {
                        setPresses(value as OptionType[])
                    }}
                    isClearable
                />
                <div className="text-sm text-gray-600">미 선택 - 전체 카테고리</div>
            </div>
            <div>
                <Link
                    to={`/wordcloud?${queryString}`}
                >
                    <button type="button" className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                        Update
                    </button>
                </Link>
            </div>
        </div>
    )
}

export default ControlPanel