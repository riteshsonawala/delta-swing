package com.deltaswing.data.worker

import android.Manifest
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat
import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.deltaswing.DeltaSwingApp
import com.deltaswing.R
import com.deltaswing.domain.repository.AuthRepository
import com.deltaswing.domain.repository.StockRepository
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject
import kotlinx.coroutines.flow.first

@HiltWorker
class StockPriceCheckWorker @AssistedInject constructor(
    @Assisted appContext: Context,
    @Assisted workerParams: WorkerParameters,
    private val stockRepository: StockRepository,
    private val authRepository: AuthRepository
) : CoroutineWorker(appContext, workerParams) {

    override suspend fun doWork(): Result {
        val user = authRepository.currentUser ?: return Result.success()
        val userId = user.uid

        stockRepository.refreshPrices(userId)

        val stocks = stockRepository.getStocks(userId).first()
        var notificationId = 1000

        stocks.filter { it.isBelowThreshold }.forEach { stock ->
            val changePercent = stock.priceChangePercent?.let {
                String.format("%.1f", kotlin.math.abs(it))
            } ?: "?"

            val title = "\uD83D\uDCC9 ${stock.symbol} Alert"
            val message = "${stock.symbol} is down ${changePercent}% from your base — consider buying!"

            sendNotification(notificationId++, title, message, stock.id)
        }

        return Result.success()
    }

    private fun sendNotification(id: Int, title: String, message: String, stockId: String) {
        if (ContextCompat.checkSelfPermission(
                applicationContext,
                Manifest.permission.POST_NOTIFICATIONS
            ) != PackageManager.PERMISSION_GRANTED
        ) return

        val intent = applicationContext.packageManager
            .getLaunchIntentForPackage(applicationContext.packageName)
            ?.apply {
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
                putExtra("stock_id", stockId)
            }

        val pendingIntent = PendingIntent.getActivity(
            applicationContext,
            id,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val notification = NotificationCompat.Builder(
            applicationContext,
            DeltaSwingApp.NOTIFICATION_CHANNEL_ID
        )
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle(title)
            .setContentText(message)
            .setStyle(NotificationCompat.BigTextStyle().bigText(message))
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .setGroup("stock_alerts")
            .build()

        NotificationManagerCompat.from(applicationContext).notify(id, notification)
    }
}
