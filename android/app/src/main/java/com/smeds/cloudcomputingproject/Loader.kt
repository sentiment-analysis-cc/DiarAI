package com.smeds.cloudcomputingproject

import android.app.AlertDialog
import android.content.Context
import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.Matrix
import android.view.Gravity
import android.view.ViewGroup
import android.view.Window
import android.view.WindowManager
import android.widget.LinearLayout
import android.widget.ProgressBar
import android.widget.TextView

/**
 * Static class that allows to adapt a image or video to fit the screen, in accordance to parameters sent by server.
 * Methods require three pairs of values:
 *  - size of image (or video) in inches
 *  - translation in 100ths of inches (centi-inches?)
 *  - rotation in degrees (TODO)
 *
 *  No class is required since those are kinda-static methods
 */

object Loader {
    lateinit var dialog : AlertDialog
    /* Function to correctly set a Process Dialog, while the app is communicating with the server
           It just creates and displays the dialog, nothing more, nothing less
           Stolen from StackOverflow
         */
    fun setProgressDialog(context : Context) {
        val llPadding = 30
        val ll = LinearLayout(context)
        ll.orientation = LinearLayout.HORIZONTAL
        ll.setPadding(llPadding, llPadding, llPadding, llPadding)
        ll.gravity = Gravity.CENTER
        var llParam = LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.WRAP_CONTENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        )
        llParam.gravity = Gravity.CENTER
        ll.layoutParams = llParam
        val progressBar = ProgressBar(context)
        progressBar.isIndeterminate = true
        progressBar.setPadding(0, 0, llPadding, 0)
        progressBar.layoutParams = llParam
        llParam = LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.WRAP_CONTENT,
            ViewGroup.LayoutParams.WRAP_CONTENT
        )
        llParam.gravity = Gravity.CENTER
        val tvText = TextView(context)
        tvText.text = "Loading..."
        tvText.setTextColor(Color.parseColor("#000000"))
        tvText.textSize = 20f
        tvText.layoutParams = llParam
        ll.addView(progressBar)
        ll.addView(tvText)
        val builder: AlertDialog.Builder = AlertDialog.Builder(context)
        builder.setCancelable(true)
        builder.setView(ll)
        this.dialog = builder.create()
        this.dialog?.show()
        val window: Window? = dialog?.window
        if (window != null) {
            val layoutParams = WindowManager.LayoutParams()
            layoutParams.copyFrom(dialog.window?.attributes)
            layoutParams.width = LinearLayout.LayoutParams.WRAP_CONTENT
            layoutParams.height = LinearLayout.LayoutParams.WRAP_CONTENT
            dialog.window?.attributes = layoutParams
        }
    }

    fun dismissProgressDialog() {
        this.dialog.dismiss()
    }
}