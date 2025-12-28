import re
from typing import Optional

def clean_sku_component(component: str, max_length: int = 4) -> str:
    if not component:
        return ""
    component = component.upper()
    component = re.sub(r'[\s\W]+', '-', component) 
    component = component.strip('-')
    if len(component) > max_length:
        component = component[:max_length]

    return component

def generate_sku(
    brand_code: str,
    type_code: str,
    spec_code_1: str,
    spec_code_2: Optional[str] = None
) -> str:
    c_brand = clean_sku_component(brand_code, max_length=5)
    c_type = clean_sku_component(type_code, max_length=5)
    c_spec1 = clean_sku_component(spec_code_1, max_length=10)
    
    components = [c_brand, c_type, c_spec1]
    
    if spec_code_2:
        c_spec2 = clean_sku_component(spec_code_2, max_length=5)
        components.append(c_spec2)
    final_sku = "-".join(filter(None, components))
    if not final_sku.startswith("SKU") and final_sku:
        final_sku = f"SKU-{final_sku}"

    return final_sku