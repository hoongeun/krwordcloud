package com.krwordcloud.api.utils

import java.text.ParseException
import java.text.SimpleDateFormat
import java.util.*

class DateUtil {
    companion object {
        fun parseDate(str: String): Date? {
            return try {
                SimpleDateFormat("YYYY-MM-DD").parse(str)
            } catch (e: ParseException) {
                null;
            }
        }
    }
}
