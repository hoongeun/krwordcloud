package com.krwordcloud.api.entity

import lombok.Data
import org.springframework.data.couchbase.core.mapping.Document


@Document
@Data
data class Trend(
    val id: String,
    val size: Long,
    val graph_size: Long,
    val rank_size: Long,
    val date: String,
    val category: String,
    val press: String,
    val score: Map<String, Float>,
)
