package com.deltaswing.di

import android.content.Context
import androidx.room.Room
import com.deltaswing.data.local.dao.StockDao
import com.deltaswing.data.local.database.AppDatabase
import com.deltaswing.data.remote.api.AlphaVantageApi
import com.deltaswing.data.repository.AuthRepositoryImpl
import com.deltaswing.data.repository.StockRepositoryImpl
import com.deltaswing.domain.repository.AuthRepository
import com.deltaswing.domain.repository.StockRepository
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import java.util.concurrent.TimeUnit
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideFirebaseAuth(): FirebaseAuth = FirebaseAuth.getInstance()

    @Provides
    @Singleton
    fun provideFirestore(): FirebaseFirestore = FirebaseFirestore.getInstance()

    @Provides
    @Singleton
    fun provideAuthRepository(firebaseAuth: FirebaseAuth): AuthRepository {
        return AuthRepositoryImpl(firebaseAuth)
    }

    @Provides
    @Singleton
    fun provideAppDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "delta_swing_db"
        ).build()
    }

    @Provides
    fun provideStockDao(database: AppDatabase): StockDao = database.stockDao()

    @Provides
    @Singleton
    fun provideMoshi(): Moshi {
        return Moshi.Builder()
            .add(KotlinJsonAdapterFactory())
            .build()
    }

    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .addInterceptor(
                HttpLoggingInterceptor().apply {
                    level = HttpLoggingInterceptor.Level.BODY
                }
            )
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .build()
    }

    @Provides
    @Singleton
    fun provideAlphaVantageApi(okHttpClient: OkHttpClient, moshi: Moshi): AlphaVantageApi {
        return Retrofit.Builder()
            .baseUrl("https://www.alphavantage.co/")
            .client(okHttpClient)
            .addConverterFactory(MoshiConverterFactory.create(moshi))
            .build()
            .create(AlphaVantageApi::class.java)
    }

    @Provides
    @Singleton
    fun provideStockRepository(
        stockDao: StockDao,
        api: AlphaVantageApi,
        firestore: FirebaseFirestore
    ): StockRepository {
        return StockRepositoryImpl(stockDao, api, firestore)
    }
}
