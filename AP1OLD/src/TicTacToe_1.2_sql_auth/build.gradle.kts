plugins {
    id("java")
    id("org.springframework.boot") version "3.2.0"
    id("io.spring.dependency-management") version "1.1.4"
}

group = "org.example"
version = "1.0-SNAPSHOT"

java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-security") // включает Spring Security. Без него не будет SecurityFilterChain и фильтров. После добавления все /game/* по умолчанию начнут требовать auth
    runtimeOnly("org.postgresql:postgresql")
    testImplementation(platform("org.junit:junit-bom:5.10.0"))
    testImplementation("org.junit.jupiter:junit-jupiter")
}

tasks.test {
    useJUnitPlatform()
}

/* добавили две зависимости — data-jpa (Hibernate + репозитории) и драйвер PostgreSQL.
Без них Spring не знает как ходить в БД. После Reload IDE подтянет jakarta.persistence.*/