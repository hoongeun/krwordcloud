package com.krwordcloud.api.entity

import lombok.Data
import org.springframework.data.couchbase.core.mapping.Document
import java.util.*


@Document
@Data
data class Stats(
    val size: Long,
    val start: String,
    val end: String,
    val created_at: String,
    val updated_at: String,
    val graph_size: Long,
    val rank_size: Long,
    val categories: List<String> = ArrayList(),
    val presses: List<String> = ArrayList()
)
