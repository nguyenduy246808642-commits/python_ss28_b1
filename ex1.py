from abc import ABC, abstractmethod


class BaseEmployee(ABC):
    company_name = "Rikkei Education"
    base_salary_rate = 3000000

    def __init__(self, emp_code, full_name):
        self.emp_code = emp_code
        self.full_name = full_name
        self.__working_hours = 0

    @property
    def full_name(self):
        return self.__full_name

    @full_name.setter
    def full_name(self, value):
        self.__full_name = " ".join(value.strip().upper().split())

    @property
    def working_hours(self):
        return self.__working_hours

    def _add_working_hours(self, hours):
        if hours <= 0:
            raise ValueError(
                "Số liệu cập nhật hiệu suất không được nhỏ hơn hoặc bằng 0"
            )
        self.__working_hours += hours

    @abstractmethod
    def calculate_salary(self):
        pass

    @abstractmethod
    def update_kpi(self, progress):
        pass

    def __add__(self, other):
        if not isinstance(other, BaseEmployee):
            return NotImplemented
        return self.working_hours + other.working_hours

    def __lt__(self, other):
        if not isinstance(other, BaseEmployee):
            return NotImplemented
        return self.working_hours < other.working_hours

    @staticmethod
    def validate_employee_code(emp_code):
        return emp_code.startswith("RKE") and len(emp_code) == 10

    @classmethod
    def update_base_salary_rate(cls, new_rate):
        cls.base_salary_rate = new_rate


class Lecturer(BaseEmployee):
    def __init__(self, emp_code, full_name):
        super().__init__(emp_code, full_name)
        self.teaching_slots = 0
        self.kpi = 0

    def conduct_class(self):
        self.teaching_slots += 1
        self._add_working_hours(2)

    def update_kpi(self, progress):
        if progress <= 0:
            raise ValueError(
                "Số liệu cập nhật hiệu suất không được nhỏ hơn hoặc bằng 0"
            )
        self.kpi = progress

    def calculate_salary(self):
        return (
            self.working_hours * self.base_salary_rate
            + self.teaching_slots * 500000
        )


class AdmissionStaff(BaseEmployee):
    def __init__(self, emp_code, full_name):
        super().__init__(emp_code, full_name)
        self.revenue_generated = 0
        self.kpi_target = 100000000

    def update_kpi(self, progress):
        if progress <= 0:
            raise ValueError(
                "Số liệu cập nhật hiệu suất không được nhỏ hơn hoặc bằng 0"
            )
        self.revenue_generated += progress

    def calculate_salary(self):
        return (
            self.working_hours * self.base_salary_rate
            + self.revenue_generated * 0.05
        )


class HybridManager(Lecturer, AdmissionStaff):
    def __init__(self, emp_code, full_name):
        super().__init__(emp_code, full_name)
        self.revenue_generated = 0
        self.kpi_target = 100000000

    def update_kpi(self, progress):
        if progress <= 0:
            raise ValueError(
                "Số liệu cập nhật hiệu suất không được nhỏ hơn hoặc bằng 0"
            )
        self.revenue_generated += progress

    def calculate_salary(self):
        salary = self.working_hours * self.base_salary_rate
        salary += self.teaching_slots * 500000
        salary += self.revenue_generated * 0.05
        return salary


class VietcombankCorporateService:
    def transfer_salary(self, employee, amount):
        print("[Hệ thống VCB Corporate]: Đang kết nối tới cổng chi trả Rikkei...")
        print("Xác thực đối tác bằng Duck Typing thành công!")
        print(
            f"Ngân hàng đối tác đã giải ngân thành công số tiền: {amount:,.0f} VND tới nhân sự {employee.emp_code}."
        )


class TechcombankCorporateService:
    def transfer_salary(self, employee, amount):
        print("[Hệ thống TCB Corporate]: Đang kết nối tới cổng chi trả Rikkei...")
        print("Xác thực đối tác bằng Duck Typing thành công!")
        print(
            f"Ngân hàng đối tác đã giải ngân thành công số tiền: {amount:,.0f} VND tới nhân sự {employee.emp_code}."
        )


def execute_payroll(payment_service, employee, amount):
    try:
        payment_service.transfer_salary(employee, amount)
    except AttributeError:
        print(
            "Cổng dịch vụ ngân hàng doanh nghiệp không hợp lệ hoặc chưa được liên kết liên thông kỹ thuật"
        )


employees = []
current_employee = None

while True:
    print("\n===== RIKKEI EDUCATION HR SIMULATOR PRO =====")
    print("1. Tuyển dụng nhân sự mới")
    print("2. Xem thông tin & Kiểm tra MRO")
    print("3. Ghi nhận công nhật & Cập nhật KPI")
    print("4. Tổng hợp quỹ lương")
    print("5. Kiểm tra Overloading")
    print("6. Giải ngân lương (Duck Typing)")
    print("7. Thoát")

    choice = input("Chọn chức năng: ")

    match choice:
        case "1":
            print("\n1. Lecturer")
            print("2. Admission Staff")
            print("3. Hybrid Manager")

            emp_type = input("Chọn loại nhân sự: ")

            emp_code = input("Nhập mã nhân sự: ")

            if not BaseEmployee.validate_employee_code(emp_code):
                print("Mã nhân sự không hợp lệ!")
                continue

            full_name = input("Nhập họ tên: ")

            if emp_type == "1":
                emp = Lecturer(emp_code, full_name)
            elif emp_type == "2":
                emp = AdmissionStaff(emp_code, full_name)
            elif emp_type == "3":
                emp = HybridManager(emp_code, full_name)
            else:
                print("Loại không hợp lệ!")
                continue

            employees.append(emp)
            current_employee = emp

            print("Tuyển dụng thành công!")
            print("Tên:", emp.full_name)

        case "2":
            if current_employee is None:
                print("Chưa có nhân sự.")
                continue

            print("\n------ THÔNG TIN NHÂN SỰ ------")
            print("Loại:", type(current_employee).__name__)
            print("Công ty:", current_employee.company_name)
            print("Mã:", current_employee.emp_code)
            print("Tên:", current_employee.full_name)
            print("Giờ làm:", current_employee.working_hours)

            if isinstance(current_employee, Lecturer):
                print("Ca dạy:", current_employee.teaching_slots)

            if isinstance(current_employee, AdmissionStaff):
                print("Doanh số:", f"{current_employee.revenue_generated:,.0f}")

            print("\nMRO:")
            for cls in type(current_employee).mro():
                print(cls.__name__)

        case "3":
            if current_employee is None:
                print("Chưa có nhân sự.")
                continue

            print("1. Ghi nhận đứng lớp")
            print("2. Cập nhật KPI")

            task = input("Chọn: ")

            try:
                if task == "1":
                    if isinstance(current_employee, Lecturer):
                        current_employee.conduct_class()
                        print("Đã ghi nhận 1 ca dạy.")
                    else:
                        print("Nhân sự này không phải giảng viên.")

                elif task == "2":
                    value = float(input("Nhập giá trị KPI/Doanh số: "))
                    current_employee.update_kpi(value)
                    print("Cập nhật thành công.")

                else:
                    print("Không hợp lệ.")
            except ValueError as e:
                print(e)

        case "4":
            if current_employee is None:
                print("Chưa có nhân sự.")
                continue

            print("\n------ LƯƠNG ------")
            print("Tên:", current_employee.full_name)
            print("Loại:", type(current_employee).__name__)
            print("Lương:", f"{current_employee.calculate_salary():,.0f} VND")

        case "5":
            if current_employee is None:
                print("Chưa có nhân sự.")
                continue

            if len(employees) < 2:
                print("Cần ít nhất 2 nhân sự.")
                continue

            print("\nDanh sách:")
            for i, emp in enumerate(employees):
                print(
                    f"{i}. {emp.emp_code} - {emp.full_name} ({emp.working_hours} giờ)"
                )

            idx = int(input("Chọn nhân sự để so sánh: "))

            other = employees[idx]

            print(
                "A < B:",
                current_employee < other,
            )

            print(
                "Tổng giờ:",
                current_employee + other,
            )

        case "6":
            if current_employee is None:
                print("Chưa có nhân sự.")
                continue

            print("1. Vietcombank")
            print("2. Techcombank")

            bank = input("Chọn: ")

            amount = float(input("Nhập số tiền giải ngân: "))

            if bank == "1":
                service = VietcombankCorporateService()
            elif bank == "2":
                service = TechcombankCorporateService()
            else:
                print("Không hợp lệ.")
                continue

            execute_payroll(service, current_employee, amount)

        case "7":
            print("Cảm ơn đã sử dụng chương trình!")
            break

        case _:
            print("Lựa chọn không hợp lệ.")