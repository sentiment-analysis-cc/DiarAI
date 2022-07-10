package com.smeds.cloudcomputingproject

import android.content.SharedPreferences
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.preference.PreferenceManager
import android.util.Log
import android.view.View
import android.widget.EditText
import android.widget.TextView
import androidx.annotation.UiThread
import okhttp3.*
import java.io.IOException
import java.lang.Exception

class GetEntriesActivity : AppCompatActivity() {
    lateinit var text : TextView
    lateinit var username : String
    lateinit var prefs : SharedPreferences
    val url = "uuq3nqiwkutez37nremubegf6i0xqjsz.lambda-url.us-east-1.on.aws"


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_get_entries)

        text = findViewById(R.id.textView2)
        prefs = PreferenceManager.getDefaultSharedPreferences(this)

    }

    fun getAllEntries(view: View) {

//        title = findViewById<EditText>(R.id.text_title).text.toString()
//        entry = findViewById<EditText>(R.id.text_entry).text.toString()
        username = prefs.getString("username", "").toString()

        val client = OkHttpClient()

        val httpUrl = HttpUrl.Builder()
            .scheme("https")
            .host(url)
            .addQueryParameter("username", username)
            .addQueryParameter("type", "all")
            .build()

        Log.i("ENTRY", httpUrl.toString())

        val request = Request.Builder()
            .url(httpUrl)
            .build()

        try {
            var res = ""
            client.newCall(request).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    Log.i("ENTRY", "onFailure: ${e.message!!}")
                }

                override fun onResponse(call: Call, response: Response) {
                    response.use {
                        Log.i("ENTRY", "onSuccess")
                        if (!response.isSuccessful) throw IOException("Unexpected code $response")

                        //Log.i("ENTRY", "Response: ${response.body?.string()}")

                        res = response.body!!.string()
                        this@GetEntriesActivity.runOnUiThread(java.lang.Runnable {
                            text.text = res
                        })
                        Log.i("ENTRY", res)
                    }
                }
            })

        } catch (e : Exception) {
            Log.i("ENTRY", e.message!!)
            return
        }

    }
}