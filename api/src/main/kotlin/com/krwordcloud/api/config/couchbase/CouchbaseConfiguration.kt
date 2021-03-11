package com.krwordcloud.api.config.couchbase

import org.springframework.context.annotation.Configuration
import org.springframework.data.couchbase.config.AbstractCouchbaseConfiguration
import java.util.Properties
import java.io.FileNotFoundException


@Configuration
class CouchbaseConfiguration : AbstractCouchbaseConfiguration() {

    override fun getConnectionString(): String {
        return System.getenv("COUCHBASE_HOST") ?: "couchbase://127.0.0.1"
    }

    override fun getUserName(): String {
        return System.getenv("COUCHBASE_USER") ?: "Administrator"
    }

    override fun getPassword(): String {
        return System.getenv("COUCHBASE_PASSWORD") ?: "password"
    }

    override fun getBucketName(): String {
        return System.getenv("COUCHBASE_BUCKET") ?: "bucket"
    }
}

// FIXME: Environment variables are doens't loaded.
//@Configuration
//class CouchbaseConfiguration(private val prop: Properties) : AbstractCouchbaseConfiguration() {
//
//    override fun getConnectionString(): String {
//        try {
//            return prop.getProperty("spring.couchbase.host")
//        } catch (e: Exception) {
//            return "couchbase://127.0.0.1"
//        }
//    }
//
//    override fun getUserName(): String {
//        try {
//            return prop.getProperty("spring.couchbase.bucket.user")
//        } catch (e: Exception) {
//            return "Administrator"
//        }
//    }
//
//    override fun getPassword(): String {
//        try {
//            return prop.getProperty("spring.couchbase.bucket.password")
//        } catch (e: Exception) {
//            return "password"
//        }
//    }
//
//    override fun getBucketName(): String {
//        try {
//            return prop.getProperty("spring.couchbase.bucket.name")
//        } catch (e: Exception) {
//            return "bucket"
//        }
//    }
//
//    init {
//        val fname = "application.properties"
//        javaClass.classLoader.getResourceAsStream(fname).use {
//            prop.apply { load(it) }
//        }
//
//        println(prop.getProperty("spring.couchbase.host"))
//        println(prop.getProperty("spring.couchbase.bucket.name"))
//        println(prop.getProperty("spring.couchbase.bucket.user"))
//        println(prop.getProperty("spring.couchbase.bucket.password"))
//    }
//}
