MAPPING_SHCEMA_selected = {
  "settings": {
    "analysis": {
      "normalizer": {
        "lowercase_ascii_normalizer": {
          "type": "custom",
          "char_filter": [],
          "filter": ["lowercase", "asciifolding"]
        }
      },
      "analyzer": {
        "custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "asciifolding"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "brand": {
        "type": "keyword",
        "normalizer": "lowercase_ascii_normalizer"
      },
      "bullet_point": {
        "type": "text",
        "analyzer": "custom_analyzer"
      },
      "color": {
        "type": "text",
        "analyzer": "custom_analyzer"
      },
      "fabric_type": {
        "type": "keyword",
        "normalizer": "lowercase_ascii_normalizer"
      },
      "item_id": {
        "type": "keyword",
        "normalizer": "lowercase_ascii_normalizer"
      },
      "item_keywords": {
        "type": "keyword",
        "normalizer": "lowercase_ascii_normalizer"
      },
      "item_name": {
        "type": "text",
        "analyzer": "custom_analyzer"
      },
      "material": {
        "type": "text",
        "analyzer": "custom_analyzer"
      },
      "product_description": {
        "type": "text",
        "analyzer": "custom_analyzer"
      },
      "product_type": {
        "type": "keyword",
        "normalizer": "lowercase_ascii_normalizer"
      },
      "style": {
        "type": "text",
        "analyzer": "custom_analyzer"
      }
    }
  }
}


MAPPING_SHCEMA={
  "settings": {
    "analysis": {
      "analyzer": {
        "custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "asciifolding"]
        }
      },
      "normalizer": {
        "lowercase_ascii_normalizer": {
          "type": "custom",
          "char_filter": [],
          "filter": ["lowercase", "asciifolding"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "brand": {
        "type": "nested",
        "properties": {
          "language_tag": {"type": "keyword"},
          "value": {"type": "keyword", "normalizer": "lowercase_ascii_normalizer"}
        }
      },
      "bullet_point": {
        "type": "nested",
        "properties": {
          "language_tag": {"type": "keyword"},
          "value": {"type": "text", "analyzer": "custom_analyzer"}
        }
      },
      "color": {
        "type": "nested",
        "properties": {
          "language_tag": {"type": "keyword"},
          "standardized_values": {"type": "keyword", "normalizer": "lowercase_ascii_normalizer"},
          "value": {"type": "text", "analyzer": "custom_analyzer"}
        }
      },
      "color_code": {"type": "keyword", "normalizer": "lowercase_ascii_normalizer"},
      "country": {"type": "keyword", "normalizer": "lowercase_ascii_normalizer"},
      "domain_name": {"type": "keyword", "normalizer": "lowercase_ascii_normalizer"},
      "fabric_type": {
        "type": "nested",
        "properties": {
          "language_tag": {"type": "keyword"},
          "value": {"type": "text", "analyzer": "custom_analyzer"}
        }
      },
      "finish_type": {
        "type": "nested",
        "properties": {
          "language_tag": {"type": "keyword"},
          "value": {"type": "text", "analyzer": "custom_analyzer"}
        }
      },
      "item_dimensions": {
        "type": "object",
        "properties": {
          "height": {
            "type": "object",
            "properties": {
              "normalized_value": {
                "type": "object",
                "properties": {
                  "unit": {"type": "keyword", "normalizer": "lowercase_ascii_normalizer"},
                  "value": {"type": "float"}
                }
              },
              "unit": {"type": "keyword", "normalizer": "lowercase_ascii_normalizer"},
              "value": {"type": "float"}
            }
          },
          "length": {
            "type": "object",
            "properties": {
              "normalized_value": {
                "type": "object",
                "properties": {
                  "unit": {"type": "keyword", "normalizer": "lowercase_ascii_normalizer"},
                  "value": {"type": "float"}
                }
              },
              "unit": {"type": "keyword", "normalizer": "lowercase_ascii_normalizer"},
              "value": {"type": "float"}
            }
          },
          "width": {
            "type": "object",
            "properties": {
              "normalized_value": {
                "type": "object",
                "properties": {
                  "unit": {"type": "keyword", "normalizer": "lowercase_ascii_normalizer"},
                  "value": {"type": "float"}
                }
              },
              "unit": {"type": "keyword", "normalizer": "lowercase_ascii_normalizer"},
              "value": {"type": "float"}
            }
          }
        }
      },
      "item_id": {"type": "keyword"},
      "item_keywords": {
        "type": "nested",
        "properties": {
          "language_tag": {"type": "keyword"},
          "value": {"type": "text", "analyzer": "custom_analyzer"}
        }
      },
      "item_name": {
        "type": "nested",
        "properties": {
          "language_tag": {"type": "keyword"},
          "value": {"type": "text", "analyzer": "custom_analyzer"}
        }
      },
      "item_shape": {
        "type": "nested",
        "properties": {
          "language_tag": {"type": "keyword"},
          "value": {"type": "text", "analyzer": "custom_analyzer"}
        }
      },
      "item_weight": {
        "type": "nested",
        "properties": {
          "normalized_value": {
            "type": "object",
            "properties": {
              "unit": {"type": "keyword", "normalizer": "lowercase_ascii_normalizer"},
              "value": {"type": "float"}
            }
          },
          "unit": {"type": "keyword", "normalizer": "lowercase_ascii_normalizer"},
          "value": {"type": "float"}
        }
      },
      "main_image_id": {"type": "keyword"},
      "marketplace": {"type": "keyword", "normalizer": "lowercase_ascii_normalizer"},
      "material": {
        "type": "nested",
        "properties": {
          "language_tag": {"type": "keyword"},
          "value": {"type": "text", "analyzer": "custom_analyzer"}
        }
      },
      "model_name": {
        "type": "nested",
        "properties": {
          "language_tag": {"type": "keyword"},
          "value": {"type": "text", "analyzer": "custom_analyzer"}
        }
      },
      "model_number": {
        "type": "nested",
        "properties": {
          "value": {"type": "keyword", "normalizer": "lowercase_ascii_normalizer"}
        }
      },
      "model_year": {
        "type": "nested",
        "properties": {
          "language_tag": {"type": "keyword"},
          "value": {"type": "integer"}
        }
      },
      "node": {
        "type": "nested",
        "properties": {
          "node_id": {"type": "long"},
          "path": {"type": "text", "analyzer": "custom_analyzer"}
        }
      },
      "other_image_id": {"type": "keyword"},
      "pattern": {
        "type": "nested",
        "properties": {
          "language_tag": {"type": "keyword"},
          "value": {"type": "text", "analyzer": "custom_analyzer"}
        }
      },
      "product_description": {
        "type": "nested",
        "properties": {
          "language_tag": {"type": "keyword"},
          "value": {"type": "text", "analyzer": "custom_analyzer"}
        }
      },
      "product_type": {
        "type": "nested",
        "properties": {
          "value": {"type": "keyword", "normalizer": "lowercase_ascii_normalizer"}
        }
      },
      "spin_id": {"type": "keyword"},
      "style": {
        "type": "nested",
        "properties": {
          "language_tag": {"type": "keyword"},
          "value": {"type": "text", "analyzer": "custom_analyzer"}
        }
      },
      "3dmodel_id": {"type": "keyword"}
    }
  }
}