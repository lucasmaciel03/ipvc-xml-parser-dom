# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: xml_service.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'xml_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11xml_service.proto\x12\txmlparser\"4\n\nXMLRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x14\n\x0c\x66ile_content\x18\x02 \x01(\t\"/\n\x0bXMLResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x0f\n\x07success\x18\x02 \x01(\x08\x32P\n\x10XMLParserService\x12<\n\x0bSendXMLFile\x12\x15.xmlparser.XMLRequest\x1a\x16.xmlparser.XMLResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'xml_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_XMLREQUEST']._serialized_start=32
  _globals['_XMLREQUEST']._serialized_end=84
  _globals['_XMLRESPONSE']._serialized_start=86
  _globals['_XMLRESPONSE']._serialized_end=133
  _globals['_XMLPARSERSERVICE']._serialized_start=135
  _globals['_XMLPARSERSERVICE']._serialized_end=215
# @@protoc_insertion_point(module_scope)
