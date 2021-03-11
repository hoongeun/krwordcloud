package com.krwordcloud.api.repositories

import com.krwordcloud.api.entity.dto.Stats
import org.springframework.data.couchbase.repository.Query
import org.springframework.data.repository.CrudRepository


interface StatsRepository : CrudRepository<Stats, String> {
    // FIXME: add dummy '__id' and '__cas' for null exception problem.
    @Query("SELECT '' as __id, 1 as __cas, SUM(size) AS `size`, MIN(date) AS `start`, MAX(date) as `end`, SUM(graph_size) as `graph_size`, SUM(rank_size) as `rank_size`, ARRAY_AGG(DISTINCT category) as categories, ARRAY_AGG(DISTINCT press) as presses FROM `Trend`")
    fun findStats(): Stats
}
