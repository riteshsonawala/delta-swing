package com.deltaswing.presentation.stockdetail

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CenterAlignedTopAppBar
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.deltaswing.domain.model.PricePoint

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun StockDetailScreen(
    stockId: String,
    onNavigateBack: () -> Unit,
    onEditStock: () -> Unit,
    viewModel: StockDetailViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()

    LaunchedEffect(stockId) {
        viewModel.loadStock(stockId)
    }

    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text(uiState.stock?.symbol ?: "Stock Detail") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(onClick = onEditStock) {
                        Icon(Icons.Default.Edit, contentDescription = "Edit")
                    }
                }
            )
        }
    ) { padding ->
        if (uiState.isLoading) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding),
                contentAlignment = Alignment.Center
            ) {
                CircularProgressIndicator()
            }
        } else {
            val stock = uiState.stock ?: return@Scaffold
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(16.dp)
                    .verticalScroll(rememberScrollState())
            ) {
                // Price card
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                ) {
                    Column(modifier = Modifier.padding(20.dp)) {
                        Text(
                            text = stock.symbol,
                            style = MaterialTheme.typography.headlineMedium,
                            fontWeight = FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.height(12.dp))

                        stock.currentPrice?.let { price ->
                            Text(
                                text = "$${String.format("%.2f", price)}",
                                style = MaterialTheme.typography.displaySmall,
                                fontWeight = FontWeight.Bold,
                                color = if (stock.isBelowThreshold)
                                    MaterialTheme.colorScheme.error
                                else MaterialTheme.colorScheme.primary
                            )
                            stock.priceChangePercent?.let { change ->
                                Text(
                                    text = "${if (change >= 0) "+" else ""}${String.format("%.2f", change)}% from base",
                                    style = MaterialTheme.typography.bodyLarge,
                                    color = if (change >= 0) Color(0xFF4CAF50) else MaterialTheme.colorScheme.error
                                )
                            }
                        } ?: Text(
                            text = "Price unavailable",
                            style = MaterialTheme.typography.bodyLarge,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))

                // Details card
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                ) {
                    Column(modifier = Modifier.padding(20.dp)) {
                        Text(
                            text = "Configuration",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        DetailRow("Base Price", "$${String.format("%.2f", stock.basePrice)}")
                        DetailRow("Delta Swing", "${stock.deltaPercentage}%")
                        DetailRow("Alert Threshold", "$${String.format("%.2f", stock.thresholdPrice)}")
                        DetailRow(
                            "Status",
                            if (stock.isBelowThreshold) "BELOW THRESHOLD" else "Normal"
                        )
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))

                // Sparkline chart
                if (uiState.priceHistory.isNotEmpty()) {
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                    ) {
                        Column(modifier = Modifier.padding(20.dp)) {
                            Text(
                                text = "30-Day Price History",
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold
                            )
                            Spacer(modifier = Modifier.height(16.dp))
                            SparklineChart(
                                pricePoints = uiState.priceHistory,
                                thresholdPrice = stock.thresholdPrice,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(200.dp)
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween
                            ) {
                                Text(
                                    text = uiState.priceHistory.first().date,
                                    style = MaterialTheme.typography.bodySmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                                Text(
                                    text = uiState.priceHistory.last().date,
                                    style = MaterialTheme.typography.bodySmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun DetailRow(label: String, value: String) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Text(
            text = value,
            style = MaterialTheme.typography.bodyMedium,
            fontWeight = FontWeight.Medium
        )
    }
}

@Composable
private fun SparklineChart(
    pricePoints: List<PricePoint>,
    thresholdPrice: Double,
    modifier: Modifier = Modifier
) {
    val lineColor = MaterialTheme.colorScheme.primary
    val thresholdColor = MaterialTheme.colorScheme.error

    Canvas(modifier = modifier) {
        if (pricePoints.isEmpty()) return@Canvas

        val prices = pricePoints.map { it.close.toFloat() }
        val minPrice = (prices.min()).coerceAtMost(thresholdPrice.toFloat()) * 0.98f
        val maxPrice = (prices.max()).coerceAtLeast(thresholdPrice.toFloat()) * 1.02f
        val range = maxPrice - minPrice

        if (range <= 0) return@Canvas

        val stepX = size.width / (prices.size - 1).coerceAtLeast(1)

        // Draw threshold line
        val thresholdY = size.height - ((thresholdPrice.toFloat() - minPrice) / range * size.height)
        drawLine(
            color = thresholdColor.copy(alpha = 0.5f),
            start = Offset(0f, thresholdY),
            end = Offset(size.width, thresholdY),
            strokeWidth = 2f,
            pathEffect = androidx.compose.ui.graphics.PathEffect.dashPathEffect(
                floatArrayOf(10f, 10f)
            )
        )

        // Draw price line
        val path = Path()
        prices.forEachIndexed { index, price ->
            val x = index * stepX
            val y = size.height - ((price - minPrice) / range * size.height)
            if (index == 0) path.moveTo(x, y) else path.lineTo(x, y)
        }
        drawPath(
            path = path,
            color = lineColor,
            style = Stroke(width = 3f, cap = StrokeCap.Round)
        )

        // Draw dots at endpoints
        val firstY = size.height - ((prices.first() - minPrice) / range * size.height)
        val lastY = size.height - ((prices.last() - minPrice) / range * size.height)
        drawCircle(color = lineColor, radius = 5f, center = Offset(0f, firstY))
        drawCircle(
            color = lineColor,
            radius = 5f,
            center = Offset(size.width, lastY)
        )
    }
}
