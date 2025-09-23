# Step 2: Extract just the "last" part
# %/ Removes the trailing slash
source .env && curl -s -I -H "Authorization: Bearer $API_KEY" "${API_URL%/}/api/v1/courses?per_page=1" | grep -i link: | grep -o '[^,]*rel="last"[^,]*' | awk -F'page=' '{split($2,a,"&"); print a[1]}'

# grep -i link:
# ignore case ()-i)
# link: 
# <https://nku.instructure.com/api/v1/courses?page=1&per_page=1>; rel="current",
# <https://nku.instructure.com/api/v1/courses?page=2&per_page=1>; rel="next",
# <https://nku.instructure.com/api/v1/courses?page=1&per_page=1>; rel="first",
# <https://nku.instructure.com/api/v1/courses?page=92&per_page=1>; rel="last"

# grep -o '[^,]*rel="last"[^,]*' 
# output only the matching part (-o)
# [^,]* find except comma 

# <https://nku.instructure.com/api/v1/courses?page=92&per_page=1>; rel="last"

# awk -F'page=' '{split($2,a,"&"); print a[1]}'
# -F'page=' (Field Separator)
# $1 = <https://nku.instructure.com/api/v1/courses?
# $2 = 92&per_page=1>; rel="last"
# Split on &:
# a[1] = 92
# a[2] = per_page=1>; rel="last"