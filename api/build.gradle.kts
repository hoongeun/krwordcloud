import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
	id("org.springframework.boot") version "2.4.2"
	id("io.spring.dependency-management") version "1.0.11.RELEASE"
	kotlin("jvm") version "1.4.21"
	kotlin("plugin.spring") version "1.4.21"
	kotlin("plugin.jpa") version "1.4.21"
}

group = "com.krwordcloud.api"
version = "0.0.1-SNAPSHOT"
java.sourceCompatibility = JavaVersion.VERSION_11

repositories {
	mavenCentral()
}

dependencies {
	implementation("org.springframework.boot:spring-boot-starter-data-couchbase")
	implementation("org.springframework.boot:spring-boot-starter-data-rest")
	implementation("org.springframework.data:spring-data-couchbase:4.1.5")
	implementation("org.jetbrains.kotlin:kotlin-reflect")
	implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")
	implementation("org.hamcrest:hamcrest-library:2.2")
	implementation("com.couchbase.client:java-client:3.1.0")
	implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
	implementation("org.projectlombok:lombok:1.18.16")
	developmentOnly("org.springframework.boot:spring-boot-devtools")
	developmentOnly("ch.qos.logback:logback-classic:1.2.3")
	runtimeOnly("io.micrometer:micrometer-registry-prometheus")
	testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.withType<KotlinCompile> {
	kotlinOptions {
		freeCompilerArgs = listOf("-Xjsr305=strict")
		jvmTarget = "11"
	}
}

tasks.withType<Test> {
	useJUnitPlatform()
}
