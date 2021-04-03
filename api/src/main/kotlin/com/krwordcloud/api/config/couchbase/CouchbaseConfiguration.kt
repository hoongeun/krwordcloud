package com.krwordcloud.api.config.couchbase

import com.krwordcloud.api.entity.Stats
import org.springframework.context.annotation.Configuration
import org.springframework.data.couchbase.CouchbaseClientFactory
import org.springframework.data.couchbase.SimpleCouchbaseClientFactory
import org.springframework.data.couchbase.config.AbstractCouchbaseConfiguration
import org.springframework.data.couchbase.core.CouchbaseTemplate
import org.springframework.data.couchbase.core.convert.MappingCouchbaseConverter
import org.springframework.data.couchbase.repository.config.EnableCouchbaseRepositories
import org.springframework.data.couchbase.repository.config.RepositoryOperationsMapping


@Configuration
@EnableCouchbaseRepositories(basePackages = ["package com.krwordcloud.api.repository"])
class CouchbaseConfiguration : AbstractCouchbaseConfiguration() {

    override fun getConnectionString(): String {
        return "couchbase://${System.getenv("COUCHBASE_HOST") ?: "localhost"}"
    }

    override fun getUserName(): String {
        return System.getenv("COUCHBASE_USER") ?: "Administrator"
    }

    override fun getPassword(): String {
        return System.getenv("COUCHBASE_PASSWORD") ?: "password"
    }

    override fun getBucketName(): String {
        return "Trend"
    }

    override fun configureRepositoryOperationsMapping(baseMapping: RepositoryOperationsMapping) {
        try {
            val statsTemplate = myCouchbaseTemplate(myCouchbaseClientFactory("Stats"), MappingCouchbaseConverter())
            baseMapping.mapEntity(Stats::class.java, statsTemplate)
        } catch (e: Exception) {
            throw e
        }
    }
    // do not use couchbaseTemplate for the name of this method, otherwise the value of that been
    // will be used instead of the result from this call (the client factory arg is different)
    fun myCouchbaseTemplate(
        couchbaseClientFactory: CouchbaseClientFactory,
        mappingCouchbaseConverter: MappingCouchbaseConverter,
    ): CouchbaseTemplate {
        return CouchbaseTemplate(couchbaseClientFactory, mappingCouchbaseConverter)
    }

    // do not use couchbaseClientFactory for the name of this method, otherwise the value of that bean will
    // will be used instead of this call being made ( bucketname is an arg here, instead of using bucketName() )
    fun myCouchbaseClientFactory(bucketName: String): CouchbaseClientFactory {
        return SimpleCouchbaseClientFactory(connectionString, authenticator(), bucketName)
    }
}
