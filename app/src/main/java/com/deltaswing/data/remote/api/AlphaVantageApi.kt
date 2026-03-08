package com.deltaswing.data.remote.api

import com.deltaswing.data.remote.dto.GlobalQuoteResponse
import com.deltaswing.data.remote.dto.TimeSeriesDailyResponse
import retrofit2.http.GET
import retrofit2.http.Query

interface AlphaVantageApi {

    @GET("query")
    suspend fun getGlobalQuote(
        @Query("function") function: String = "GLOBAL_QUOTE",
        @Query("symbol") symbol: String,
        @Query("apikey") apiKey: String
    ): GlobalQuoteResponse

    @GET("query")
    suspend fun getDailyTimeSeries(
        @Query("function") function: String = "TIME_SERIES_DAILY",
        @Query("symbol") symbol: String,
        @Query("outputsize") outputSize: String = "compact",
        @Query("apikey") apiKey: String
    ): TimeSeriesDailyResponse
}
