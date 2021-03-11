package com.krwordcloud.api.utils

import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.ResponseStatus


@ResponseStatus(HttpStatus.BAD_REQUEST)
open class BadRequestException(message: String) : RuntimeException(message)

@ResponseStatus(HttpStatus.NOT_FOUND)
class NotFoundException(message: String) : BadRequestException(message)

@ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
open class InternalServerException(message: String) : RuntimeException(message)