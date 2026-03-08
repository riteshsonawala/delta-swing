package com.deltaswing.data.remote.dto

import com.squareup.moshi.Json
import com.squareup.moshi.JsonClass

@JsonClass(generateAdapter = true)
data class TimeSeriesDailyResponse(
    @Json(name = "Meta Data")
    val metaData: MetaData?,
    @Json(name = "Time Series (Daily)")
    val timeSeries: Map<String, DailyData>?
)

@JsonClass(generateAdapter = true)
data class MetaData(
    @Json(name = "1. Information")
    val information: String?,
    @Json(name = "2. Symbol")
    val symbol: String?
)

@JsonClass(generateAdapter = true)
data class DailyData(
    @Json(name = "1. open")
    val open: String?,
    @Json(name = "2. high")
    val high: String?,
    @Json(name = "3. low")
    val low: String?,
    @Json(name = "4. close")
    val close: String?,
    @Json(name = "5. volume")
    val volume: String?
)
