package com.smeds.cloudcomputingproject

import android.content.Context
import android.content.SharedPreferences
import android.os.Bundle
import android.preference.PreferenceManager
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import okhttp3.*
import java.io.IOException


class GetEntriesActivity : AppCompatActivity(), EntryRecyclerAdapter.EntryClickListener {
    lateinit var text : TextView
    lateinit var username : String
    lateinit var prefs : SharedPreferences
    lateinit var recyclerViewAdapter: EntryRecyclerAdapter
    val url = "uuq3nqiwkutez37nremubegf6i0xqjsz.lambda-url.us-east-1.on.aws"


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_get_entries)

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
                            populateRecyclerView(res)
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

    fun populateRecyclerView(res: String) {
        Log.i("ENTRY", "$res")

        val entryList: List<DiaryEntry> = Gson().fromJson(res, object : TypeToken<ArrayList<DiaryEntry?>?>() {}.type)
        Log.i("ENTRY", "EntryList: ${entryList.count()}")

        // Manually add Date to each entry
        for (entry in entryList) {
            entry.date = entry.parseDate(entry.id)
        }

        // Populate RecyclerView
        val recyclerView = findViewById<RecyclerView>(R.id.recyclerView)
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerViewAdapter = EntryRecyclerAdapter(this, entryList)
        recyclerViewAdapter.listener = (object : EntryRecyclerAdapter.EntryClickListener {
            override fun onItemClick(view: View, id: String) {
                Toast.makeText(this@GetEntriesActivity, "Clicked: ${id}", Toast.LENGTH_SHORT).show()
            }
        })
        recyclerView.adapter = recyclerViewAdapter
        recyclerView.visibility = View.VISIBLE
        Log.i("ENTRY", "RecyclerView populated")
    }

    override fun onItemClick(view: View, id: String) {
        Log.i("ENTRY", "Clicked: $id")
    }
}

