# Moshi
-keep class com.deltaswing.data.remote.dto.** { *; }
-keepclassmembers class com.deltaswing.data.remote.dto.** { *; }

# Keep Moshi adapters
-keep class com.squareup.moshi.** { *; }
-keepclassmembers class * {
    @com.squareup.moshi.Json <fields>;
}
