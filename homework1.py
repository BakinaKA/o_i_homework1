class Subject:
    def __init__(self, subject_name, lecture_count, laboratory_count, practice_count):
        self._subject_name=subject_name
        self._lecture_count=lecture_count
        self._laboratory_count=laboratory_count
        self._practice_count=practice_count
    def info(self):
        print(self._subject_name)
        print(self._lecture_count)
        print(self._laboratory_count)
        print(self._practice_count)
        return

def calculate_cost_of_teachers(teacher_salary,subject_count, total_class_time):
    cost=0
    full_rate_teachers_count=int((subject_count+1.5)/3+0.5)
    full_lessons_per_school_time=10*4*8
    half_lessons_per_school_time=5*4*8
    accessible_time=full_rate_teachers_count*full_lessons_per_school_time
    part_time_rate_teachers_count=0
    if total_class_time>accessible_time:
        full_rate_teachers_count=int((total_class_time+full_lessons_per_school_time/2)/full_lessons_per_school_time+0.5)
        part_time_rate_teachers_count=int((total_class_time-full_rate_teachers_count*full_lessons_per_school_time +half_lessons_per_school_time/2)/half_lessons_per_school_time+0.5)
    else:
        if total_class_time<accessible_time:
            free_time=accessible_time-total_class_time
            part_time_rate_teachers_count=int(free_time/half_lessons_per_school_time)
            if part_time_rate_teachers_count>full_rate_teachers_count:
                part_time_rate_teachers_count=full_rate_teachers_count
                full_rate_teachers_count=0
            else:
                full_rate_teachers_count-=part_time_rate_teachers_count
    cost= teacher_salary*full_rate_teachers_count+part_time_rate_teachers_count*0.5*teacher_salary
    return (cost,full_rate_teachers_count+part_time_rate_teachers_count)

def reading_data(path_to_file):
    file = open(path_to_file, "r")
    Subject_List=[]
    words = file.read().split()
    for i in range(0,int(len(words)), 4):
           Subject_List.append(Subject(words[i],int(words[i+1]),int(words[i+2]),int(words[i+3])))
    file.close()
    return Subject_List

def calculate_total_class_time(Subject_List, count_band):
    total_lecture_count=0
    total_laboratory_count=0
    total_practice_count=0
    for tmp in Subject_List:
        total_lecture_count+=tmp._lecture_count
        total_laboratory_count+=tmp._laboratory_count
        total_practice_count+=tmp._practice_count
    return (total_lecture_count,total_laboratory_count,total_practice_count)

def calculate_internet_costs(is_distant, count_user, internet_cost):
    if(is_distant):
        return internet_cost*count_user
    else:
        return (count_user+2.5)/5 * internet_cost

def calculate_cost_required_area_for_students(rent_price,number_of_couples, number_of_students,count_band,workplace_area, utility_payments):
    area=workplace_area*number_of_students
    slots=7*6*4
    couples_in_month=number_of_couples/8
    count_area=int((count_band*couples_in_month+slots/2)/slots+0.5)
    return (count_area,count_area*area*rent_price*12+utility_payments*count_area*area*12)

def calculate_cost_equipment(equipment_cost,inflation, year):
    for i in range(0,year):
        equipment_cost+=inflation*equipment_cost
    return equipment_cost/year

def calculate_all(is_distant,path,teacher_salary,system_administrator_salary,booker_salary,
                  methodist_salary,security_guard_salary, cleaner_salary, costs_for_1C, inflation,
                  band_size,count_band,rent_price,computer_cost,projector_cost,office_cost,internet_cost, 
                  workplace_area, utility_payments,table_cost,chair_cost):
    Subject_List=reading_data(path);
    class_time=calculate_total_class_time(Subject_List,count_band)
    total_lecture_count=class_time[0]
    total_laboratory_count=class_time[1]
    total_practice_count=class_time[2]
    total_class_time=total_lecture_count+total_laboratory_count+total_practice_count
    result=0
    pair=calculate_cost_of_teachers(teacher_salary,len(Subject_List),total_class_time)
    number_of_teachers=pair[1]
    result+=(pair[0]+system_administrator_salary*12+booker_salary*2*12+methodist_salary*2*12+security_guard_salary*3*12+cleaner_salary*12)*1.301
    number_of_computer=number_of_teachers+5 
    if not is_distant:
        number_of_computer+=int(band_size*count_band/2)
    new_computer_cost=calculate_cost_equipment(computer_cost,inflation,5)
    result+=number_of_computer*new_computer_cost
    number_of_table=0
    if is_distant:
        result+=(number_of_teachers+7)*workplace_area*rent_price*12+(number_of_teachers+7)*workplace_area*utility_payments*12
    else:
        pair=calculate_cost_required_area_for_students(rent_price,total_laboratory_count+total_practice_count,band_size,count_band,workplace_area,utility_payments)
        result+=pair[1]+(number_of_teachers+7)*workplace_area*rent_price*12+(number_of_teachers+7)*workplace_area*utility_payments*12
        number_of_table=band_size*count_band*pair[0]
        pair=calculate_cost_required_area_for_students(rent_price,total_lecture_count,count_band*band_size,1,workplace_area,utility_payments)
        result+=pair[1]+(number_of_teachers+7)*workplace_area*rent_price*12+(number_of_teachers+7)*workplace_area*utility_payments*12
        number_of_projector_cost=pair[0]
        number_of_table+=band_size*count_band*pair[0]
    if not is_distant:
        new_projector_cost=calculate_cost_equipment(projector_cost, inflation,5)
        result+=number_of_projector_cost*new_projector_cost
    number_of_chair=number_of_table
    if not is_distant:
        result+=number_of_table*calculate_cost_equipment(table_cost,inflation,20)+number_of_chair*calculate_cost_equipment(chair_cost,inflation,20)
    result+=(number_of_teachers+5)*office_cost*12
    result+=costs_for_1C
    result+=calculate_internet_costs(is_distant,number_of_teachers+5,internet_cost)
    result+=result*inflation
    return int(result/(band_size*count_band)+0/5)

if __name__ =="__main__":
    teacher_salary=100000
    system_administrator_salary=70000
    booker_salary=65000
    inflation=0.067
    rent_price=400
    internet_cost=650
    methodist_salary=65000
    security_guard_salary=30000
    cleaner_salary=35000
    costs_for_1C=40000

    computer_cost=100000
    projector_cost=13000
    office_cost=3000
    workplace_area=4
    utility_payments=150
    table_cost=1000
    chair_cost=800
    print("Стоимость дистанционного обучения, если в группе 12 студентов:")
    print(calculate_all(True,"subject.txt",teacher_salary,system_administrator_salary,booker_salary,
                      methodist_salary,security_guard_salary, cleaner_salary, costs_for_1C, inflation,
                      12,7,rent_price,computer_cost,projector_cost,office_cost,internet_cost, workplace_area, utility_payments,table_cost,chair_cost))
    print("Стоимость очного обучения, если в группе 12 студентов:")
    print(calculate_all(False,"subject.txt",teacher_salary,system_administrator_salary,booker_salary,
                      methodist_salary,security_guard_salary, cleaner_salary, costs_for_1C, inflation,
                      12,7,rent_price,computer_cost,projector_cost,office_cost,internet_cost, workplace_area, utility_payments,table_cost,chair_cost))
    print("Стоимость дистанционного обучения, если в группе 22 студентов:")
    print(calculate_all(True,"subject.txt",teacher_salary,system_administrator_salary,booker_salary,
                      methodist_salary,security_guard_salary, cleaner_salary, costs_for_1C, inflation,
                      22,4,rent_price,computer_cost,projector_cost,office_cost,internet_cost, workplace_area, utility_payments,table_cost,chair_cost))
    print("Стоимость очного обучения, если в группе 22 студентов:")
    print(calculate_all(False,"subject.txt",teacher_salary,system_administrator_salary,booker_salary,
                      methodist_salary,security_guard_salary, cleaner_salary, costs_for_1C, inflation,
                      22,4,rent_price,computer_cost,projector_cost,office_cost,internet_cost, workplace_area, utility_payments,table_cost,chair_cost))
    