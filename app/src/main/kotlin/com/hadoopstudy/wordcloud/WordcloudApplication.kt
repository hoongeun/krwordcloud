package com.hadoopstudy.wordcloud

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class WordcloudApplication

fun main(args: Array<String>) {
	runApplication<WordcloudApplication>(*args)
}
