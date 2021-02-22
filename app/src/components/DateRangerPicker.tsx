import React from "react";
import moment, { Moment } from "moment";
import { omit } from "lodash";
import {
  DateRangePickerShape,
  isInclusivelyAfterDay,
  DateRangePicker,
  FocusedInputShape,
} from "react-dates";
import "react-dates/initialize";
import "react-dates/lib/css/_datepicker.css";

const defaultProps: Omit<
  DateRangePickerShape,
  "startDate" | "endDate" | "onDatesChange" | "focusedInput" | "onFocusChange"
> & {
  autoFocus: boolean;
  autoFocusEndDate: boolean;
  stateDateWrapper: (date: Moment | null) => Moment | null;
} = {
  // example props for the demo
  autoFocus: false,
  autoFocusEndDate: false,

  // input related props
  startDateId: "startDate",
  startDatePlaceholderText: "Start Date",
  endDateId: "endDate",
  endDatePlaceholderText: "End Date",
  disabled: false,
  required: false,
  screenReaderInputMessage: "",
  showClearDates: false,
  showDefaultInputIcon: false,
  customInputIcon: null,
  customArrowIcon: null,
  customCloseIcon: null,
  block: false,
  small: false,
  regular: false,

  // calendar presentation and interaction related props
  renderMonthText: null,
  renderMonthElement: undefined,
  orientation: "horizontal",
  anchorDirection: "left",
  horizontalMargin: 0,
  withPortal: false,
  withFullScreenPortal: false,
  initialVisibleMonth: null,
  numberOfMonths: 2,
  keepOpenOnDateSelect: false,
  reopenPickerOnClearDates: false,
  isRTL: false,

  // navigation related props
  navPosition: "navPositionTop",
  navPrev: null,
  navNext: null,
  onPrevMonthClick() {},
  onNextMonthClick() {},
  onClose() {},

  // day presentation and interaction related props
  renderCalendarDay: undefined,
  renderDayContents: null,
  minimumNights: 1,
  enableOutsideDays: false,
  isDayBlocked: () => false,
  isOutsideRange: (day: Moment) => !isInclusivelyAfterDay(day, moment()),
  isDayHighlighted: () => false,

  // internationalization
  displayFormat: () => moment.localeData().longDateFormat("L"),
  monthFormat: "MMMM YYYY",

  stateDateWrapper: (date: Moment | null) => date,
};

type DateRangePickerProps = Partial<
  Omit<
    DateRangePickerShape,
    "startDate" | "endDate" | "focusedInput" | "onFocusChange"
  > & {
    autoFocus: boolean;
    autoFocusEndDate: boolean;
    stateDateWrapper: (date: Moment | null) => Moment | null;
  }
> & {
  startDate: Moment;
  endDate: Moment;
  onDatesChange: typeof DateRangePickerShape.onDatesChange;
};

const DateRangePickerWrapper: React.FC<DateRangePickerProps> = (props) => {
  const [focusedInput, setFocusedInput] = React.useState<
    "startDate" | "endDate" | null
  >(props.autoFocus ? "startDate" : props.autoFocusEndDate ? "endDate" : null);

  // autoFocus, autoFocusEndDate, initialStartDate and initialEndDate are helper props for the
  // example wrapper but are not props on the SingleDatePicker itself and
  // thus, have to be omitted.
  const omittedProps = omit(props, [
    "autoFocus",
    "autoFocusEndDate",
    "stateDateWrapper",
    "startDate",
    "endDate",
  ]) as Omit<DateRangePickerShape, "focusedInput" | "onFocusChange"> & {
    autoFocus: boolean;
    autoFocusEndDate: boolean;
    stateDateWrapper: (date: Moment | null) => Moment | null;
    startDate: Moment;
    endDate: Moment;
    onChange: typeof DateRangePickerShape.onDatesChange;
  };

  return (
    <DateRangePicker
      // renderMonthText={month => month.format('MMM')}
      {...omittedProps}
      onFocusChange={(focusedInput: FocusedInputShape | null) => {
        setFocusedInput(focusedInput);
      }}
      focusedInput={focusedInput}
      startDate={props.startDate}
      endDate={props.endDate}
      renderMonthText={null}
      renderMonthElement={undefined}
    />
  );
};

DateRangePickerWrapper.defaultProps = defaultProps;

export default DateRangePickerWrapper;
