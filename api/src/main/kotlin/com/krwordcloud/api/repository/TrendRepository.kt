package com.krwordcloud.api.repository

import com.krwordcloud.api.entity.Trend
import org.springframework.data.couchbase.repository.CouchbaseRepository
import org.springframework.data.couchbase.repository.Query


interface TrendRepository : CouchbaseRepository<Trend, String> {
    @Query("#{#n1ql.selectEntity} WHERE #{#n1ql.filter} and `date` BETWEEN $1 AND $2 AND (`category` IN $3 OR IFMISSINGORNULL($3,\"\") = \"\") AND (`press` IN \$4 OR IFMISSINGORNULL(\$4,\"\") = \"\") ORDER BY DATE") // it works
    fun findByRange(start: String, end: String, categories: List<String>?, presses: List<String>?): List<Trend>
}
