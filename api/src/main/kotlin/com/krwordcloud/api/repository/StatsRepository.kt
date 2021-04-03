package com.krwordcloud.api.repository

import com.krwordcloud.api.entity.Stats
import org.springframework.data.couchbase.repository.Query
import org.springframework.data.repository.CrudRepository


interface StatsRepository : CrudRepository<Stats, String> {
    @Query("#{#n1ql.selectEntity} WHERE #{#n1ql.filter} ORDER BY updated_at DESC LIMIT 1")
    fun findLatestStats(): Stats
}
