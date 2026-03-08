package com.deltaswing.presentation.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext

private val DarkColorScheme = darkColorScheme(
    primary = Color(0xFF80CBC4),
    onPrimary = Color(0xFF003731),
    primaryContainer = Color(0xFF004F47),
    onPrimaryContainer = Color(0xFF9EF2E8),
    secondary = Color(0xFFB1CCC7),
    onSecondary = Color(0xFF1C3531),
    secondaryContainer = Color(0xFF334B47),
    onSecondaryContainer = Color(0xFFCDE8E3),
    tertiary = Color(0xFFADCAE5),
    onTertiary = Color(0xFF153349),
    tertiaryContainer = Color(0xFF2D4A61),
    onTertiaryContainer = Color(0xFFCAE6FF),
    error = Color(0xFFFFB4AB),
    surface = Color(0xFF0F1513),
    onSurface = Color(0xFFDFE4E1),
    surfaceVariant = Color(0xFF3F4946),
    onSurfaceVariant = Color(0xFFBFC9C5)
)

private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF006B5F),
    onPrimary = Color.White,
    primaryContainer = Color(0xFF9EF2E8),
    onPrimaryContainer = Color(0xFF00201C),
    secondary = Color(0xFF4A635E),
    onSecondary = Color.White,
    secondaryContainer = Color(0xFFCDE8E3),
    onSecondaryContainer = Color(0xFF06201C),
    tertiary = Color(0xFF45617A),
    onTertiary = Color.White,
    tertiaryContainer = Color(0xFFCAE6FF),
    onTertiaryContainer = Color(0xFF001E31),
    error = Color(0xFFBA1A1A),
    surface = Color(0xFFFAFDFA),
    onSurface = Color(0xFF191C1B),
    surfaceVariant = Color(0xFFDBE5E1),
    onSurfaceVariant = Color(0xFF3F4946)
)

@Composable
fun DeltaSwingTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context)
            else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        content = content
    )
}
