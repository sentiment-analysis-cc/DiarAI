package com.smeds.cloudcomputingproject

import android.util.Log
import java.lang.Integer.parseInt
import java.text.SimpleDateFormat

class DiaryEntry(var id: String, var username: String, var title: String, var sentiment : Sentiment) {

    var date : String


    init {
        this.date = parseDate(id)
    }

    fun parseDate(id: String): String {
        val d = parseInt(id.split("/")[1].split(".")[0])
        val sdf = SimpleDateFormat("dd/MM/yyyy HH:mm")

        val result = sdf.format(d * 1000L)
        Log.i("DiaryEntry", "Date: $result")
        return result
    }

    class Sentiment(
        var neg : Float,
        var pos : Float,
        var compound : Float,
        var neu : Float
        ) {

        override fun toString(): String {
            return "$compound"
        }
    }

}