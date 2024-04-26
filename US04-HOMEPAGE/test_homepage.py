from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import pytest
import json
from time import sleep
from constants.globalConstants import *
from pathlib import Path



class Test_Homepage:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()                
        self.driver.get(LOGIN_URL)
        existing_folder_path= "images"
        self.folderPath= existing_folder_path#str("screenshots") 
        Path(self.folderPath).mkdir(parents=True, exist_ok=True) #klasörü oluşturmak için ve o klasördeki veriyi korumak için
        yield
        self.driver.quit()

    def waitForElementVisible(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(locator))
    
    
    def homepage_btn_click(self):
        homepage_nav_button=self.waitForElementVisible((By.XPATH, HOMEPAGE_NAV_XPATH))
        homepage_nav_button.click()
        sleep(2)
        self.driver.execute_script("window.scrollTo(0,1000)")
        sleep(2)
        
    #anasayfa'ya yönlendirme bildirimi kontrolü
    def test_successful_login(self): 
        email = self.waitForElementVisible((By.NAME, EMAIL_NAME))
        password = self.waitForElementVisible((By.NAME, PASSWORD_NAME))
        email.send_keys(tobeto_email)
        password.send_keys(tobeto_password)
        loginBtn=self.waitForElementVisible((By.XPATH, LOGINBUTTON_XPATH))
        loginBtn.click()
        sleep(2)
        successLogin=self.waitForElementVisible((By.XPATH, SUCCESSFUL_LOGIN_TEXT_XPATH))
        assert "• Giriş başarılı." in successLogin.text and self.driver.current_url == HOMEPAGE_URL
        
    
    def test_top_menu_navigate(self): 
        self.test_successful_login()
        self.driver.save_screenshot(f"{self.folderPath}/selected_homepage.png")
        sleep(2)
        profile=self.waitForElementVisible((By.XPATH, PROFILE_XPATH))
        profile.click()
        sleep(2)
        assessments=self.waitForElementVisible((By.XPATH,ASSESSMENTS_XPATH))
        assessments.click()
        catalog=self.waitForElementVisible((By.XPATH,CATALOG_XPATH))
        catalog.click()
        calendar=self.waitForElementVisible((By.XPATH, CALENDAR_XPATH))
        calendar.click()
        istanbul_kodluyor=self.waitForElementVisible((By.XPATH,ISTANBUL_K_XPATH))
        istanbul_kodluyor.click()
        assert{self.driver.current_url==PROFILE_URL and 
               self.driver.current_url==ASSESSMENTS_URL and 
               self.driver.current_url==CATALOG_URL and 
               self.driver.current_url==CALENDAR_URL and 
               self.driver.current_url==ISTANBUL_K_URL}
    
    
    def test_welcome_and_ik(self):
        self.test_successful_login()
        sleep(2)
        welcometobeto = self.waitForElementVisible((By.XPATH, WELCOMETOBETO_XPATH))
        tobeto_slogan=self.waitForElementVisible((By.XPATH, TOBETO_SLOGAN_XPATH))
        istanbul_kodluyor_logo=self.waitForElementVisible((By.CSS_SELECTOR, ISTANBUL_KODLUYOR_LOGO_CSS_SELECTOR)) #logo görüntülenmesi için
        name=self.waitForElementVisible((By.XPATH, NAME_XPATH))
        sleep(2)
        self.driver.execute_script("window.scrollTo(0,300)")
        sleep(2)
        free_edu=self.waitForElementVisible((By.XPATH, FREE_EDUC_XPATH))
        aradığın_is_burada = self.waitForElementVisible((By.XPATH, ARADIGIN_IS_XPATH))

        assert {welcometobeto.text == WELCOMETOBETO_TEXT  and 
                name.text=="Sevda" and
                istanbul_kodluyor_logo.is_displayed(), "Logo görüntülenmiyor." and #eğer logo görüntülenmezse virgülden sonraki uyarıyı verecek.
                tobeto_slogan.text == TOBETO_SLOGAN_TEXT and 
                free_edu.text == FREE_EDUC_TEXT and
                aradığın_is_burada.text == ARADIGIN_IS_TEXT}
    
  
    def test_istanbul_is_coding_panel(self):
        self.test_successful_login()
        self.driver.execute_script("window.scrollTo(0,500)")
        apply_Btn=self.waitForElementVisible((By.ID, APPLY_ID))
        ariaSelected_Value=apply_Btn.get_attribute("aria-selected")
        sleep(2)
        myLessons=self.waitForElementVisible((By.ID, LESSONS_ID))
        myLessons.click()
        myLessonsContent=self.waitForElementVisible((By.ID, LESSONS_CONTENT_ID))
        sleep(2)
        notification=self.waitForElementVisible((By.ID, ANNOUNCEMENT_AND_NEWS_ID))
        no_read_announcements=self.waitForElementVisible((By.XPATH, NO_READ_ANNOUNCEMENT_XPATH))
        notification.click()
        sleep(2)
        notificationContent=self.waitForElementVisible((By.ID, ANNOUNCEMENT_AND_NEWS_CONTENT_ID))
        sleep(2)
        mySurveys=self.waitForElementVisible((By.ID, SURVEY_ID))
        mySurveys.click()
        sleep(2)
        mySurveysContent=self.waitForElementVisible((By.ID, SURVEY_CONTENT_ID))

        assert {ariaSelected_Value=="true" and
                myLessonsContent.is_displayed(), "Eğitimlerim içeriği görüntülenmiyor." and
                notificationContent.is_displayed(), "Duyurular ve Haberlerim görüntülenmiyor." and no_read_announcements.text=="1" and
                mySurveysContent.text==NO_SURVEY_TEXT

               }
    
    
    def test_my_educations(self): 
        self.test_successful_login()
        self.driver.execute_script("window.scrollTo(0,700)")
        sleep(2)
        myLessons_btn=self.waitForElementVisible((By.ID, LESSONS_ID))
        myLessons_btn.click()
        shown_lessons=self.driver.find_elements(By.ID, ALL_LESSONS_ID)
        sleep(2)
        showMoreBtn=self.waitForElementVisible((By.XPATH, SHOWMORE_BTN_LESSONS_XPATH))
        showMoreBtn.click()  
        sleep(2)
        go_to_lesson_button=self.waitForElementVisible((By.XPATH, GOTO_LESSON_XPATH))  #herkes için kodlama-3a seçildi
        go_to_lesson_button.click()
        sleep(3)
        details=self.waitForElementVisible((By.XPATH, DETAILS_XPATH))

        self.driver.save_screenshot(f"{self.folderPath}/details_lesson.png")
        assert {len(shown_lessons)<=4, "4'ten fazla ders görüntülendi." and
                self.driver.current_url==LESSONS_URL and
                details.text==DETAILS_TEXT  #eğitime git butonuna tıkladıktan sonra açılan sayfada görmek istediğim içerik
                }
       
    def test_announcement_and_news(self): 
        self.test_successful_login()
        self.driver.execute_script("window.scrollTo(0,500)")
        sleep(2)
        announc_and_news_btn=self.waitForElementVisible((By.ID, ANNOUNCEMENT_AND_NEWS_ID))
        announc_and_news_btn.click()
        shown_announc_and_news=self.driver.find_elements(By.ID, ANNOUNCEMENT_AND_NEWS_CONTENT_ID)
        sleep(2)
        show_more_button=self.waitForElementVisible((By.XPATH, SHOWMORE_BTN_ANNOUNCEMENT_AND_NEWS_XPATH))
        sleep(2)
        show_more_button.click()  
        sleep(2)
        read_more_button=self.waitForElementVisible((By.XPATH, READ_MORE_BUTTON_XPATH))
        read_more_button.click()
        sleep(2)
        about_clickBtn=self.waitForElementVisible((By.XPATH, ABOUT_CLICK_BUTTON_XPATH))

        assert { len(shown_announc_and_news)<=3, "3'ten fazla ders görüntülendi." and
                 self.driver.current_url==ANNOUNCEMENTS_URL
               }
    
    def test_my_exams(self): 
        self.test_successful_login()
        self.driver.execute_script("window.scrollTo(0,500)")
        exams=self.waitForElementVisible((By.XPATH, EXAMS_XPATH))
        exams_content=self.waitForElementVisible((By.XPATH, EXAMS_CONTENT_XPATH))
        sleep(2)
        exam_Btn=self.waitForElementVisible((By.XPATH, EXAMS_BUTTON_XPATH))       
        exam_Btn.click()
        exam_window=self.waitForElementVisible((By.XPATH, EXAMS_WİNDOW_XPATH))
        view_the_report_Btn=self.waitForElementVisible((By.XPATH, VIEW_THE_REPORT_BUTTON_XPATH))
        view_the_report_Btn.click()
        report_popup=self.waitForElementVisible((By.XPATH, REPORT_POPUP_XPATH))

        assert{exams.text=="Sınavlarım" and
               exams_content.text== EXAMS_CONTENT_TEXT and
               exam_window.is_displayed(), "Sınava ait detaylar görüntülenmedi" and
               report_popup.text== REPORT_POPUP_TEXT #niye 0 var?
              }

        


   
    def test_bottom_ofthe_homepage(self):  
        self.test_successful_login()
        self.driver.execute_script("window.scrollTo(0,1000)")
        sleep(2)
        areaContol=self.waitForElementVisible((By.XPATH, AREA_CONTROL_BOTTOM_XPATH))
        areaContol.text==AREA_CONTROL_BOTTOM_TEXT
        cr_profile_btn=self.waitForElementVisible((By.XPATH, CR_PROFILE_BUTTON_XPATH))
        cr_profile_btn.click()
        sleep(2)
        #expected_url=PROFİLE_INFO_URL
        self.homepage_btn_click()
        self.driver.execute_script("window.scrollTo(0,1000)")
        imp_yourself_btn=self.waitForElementVisible((By.XPATH,IMP_YOURSELF_BTN_XPATH ))
        imp_yourself_btn.click()
        self.homepage_btn_click()
        sleep(2)
        start_to_learn_btn=self.waitForElementVisible((By.XPATH, START_TO_LEARN_BTN_XPATH))
        start_to_learn_btn.click()
        expected_url= "https://tobeto.com/egitimlerim"
        
        assert {areaContol.text==AREA_CONTROL_BOTTOM_TEXT and
                self.driver.current_url==PROFILE_INFO_URL and
                self.driver.current_url==IMP_YOURSELF_URL and
                self.driver.current_url==expected_url 
               }
      





