from pydantic import BaseModel

class TemplateMapping(BaseModel):
    table_column: str
    '''
    The column name of the table file
    '''
    template_column: str
    '''
    The column name of the template file
    '''
    reason: str
    '''
    The reason for the mapping
    '''

class TemplateMappingList(BaseModel):
    template_mappings: list[TemplateMapping]
    '''
    A list of TemplateMapping objects
    '''



class TemplateMappingCode(BaseModel):
    table_column: str
    '''
    The column name of the table file
    '''
    template_column: str
    '''
    The column name of the template file
    '''
    code: str
    '''
    The code to transform the format of values table column to the format of values in template column
    '''

class TemplateMappingCodeList(BaseModel):
    template_mapping_codes: list[TemplateMappingCode]
    '''
    A list of TemplateMappingCode objects
    '''

class TransformValue(BaseModel):
    source: str
    destination: str