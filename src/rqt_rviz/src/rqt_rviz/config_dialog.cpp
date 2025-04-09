/*
 * Copyright (c) 2018, Open Source Robotics Foundation, Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 *   * Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *   * Redistributions in binary form must reproduce the above
 *     copyright notice, this list of conditions and the following
 *     disclaimer in the documentation and/or other materials provided
 *     with the distribution.
 *   * Neither the name of the TU Darmstadt nor the names of its
 *     contributors may be used to endorse or promote products derived
 *     from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#include <QFileDialog>
#include <QGridLayout>
#include <QLabel>
#include <QPushButton>

#include <rqt_rviz/config_dialog.h>

namespace rqt_rviz {

ConfigDialog::ConfigDialog()
{
  // Window configurations
  this->setWindowTitle(tr("Choose configuration"));
  this->setWindowFlags(Qt::Window | Qt::WindowCloseButtonHint |
      Qt::WindowStaysOnTopHint | Qt::CustomizeWindowHint);

  // File
  QLabel* file_label = new QLabel("File path");
  file_label->setToolTip("Full path to file");

  file_edit_ = new QLineEdit;
  file_edit_->setMinimumWidth(300);

  QPushButton* browse_button = new QPushButton(tr("Browse"));
  connect(browse_button, SIGNAL(clicked()), this, SLOT(OnBrowse()));

  // Hide menu
  QLabel* hide_label = new QLabel("Hide menu");
  hide_label->setToolTip("Check to hide RViz's top menu bar");

  hide_box_ = new QCheckBox();

  // Buttons
  QPushButton* cancel_button = new QPushButton(tr("&Cancel"));
  this->connect(cancel_button, SIGNAL(clicked()), this, SLOT(close()));

  QPushButton* apply_button = new QPushButton(tr("&Apply"));
  apply_button->setDefault(true);
  this->connect(apply_button, SIGNAL(clicked()), this, SLOT(accept()));

  QHBoxLayout* buttons_layout = new QHBoxLayout;
  buttons_layout->addWidget(cancel_button);
  buttons_layout->addWidget(apply_button);

  // Layout
  QGridLayout* main_layout = new QGridLayout();

  main_layout->addWidget(file_label, 0, 0);
  main_layout->addWidget(file_edit_, 0, 1);
  main_layout->addWidget(browse_button, 0, 2);

  main_layout->addWidget(hide_label, 1, 0);
  main_layout->addWidget(hide_box_, 1, 1);
  main_layout->setAlignment(hide_box_, Qt::AlignLeft);

  main_layout->addLayout(buttons_layout, 2, 0, 1, 3);
  main_layout->setColumnStretch(1, 2);

  this->setLayout(main_layout);
}

ConfigDialog::~ConfigDialog()
{
}

void ConfigDialog::OnBrowse()
{
  QString filename = QFileDialog::getOpenFileName(0,
    tr("Choose config file:"), "", tr("Rviz config file (*.rviz)"));

  file_edit_->setText(filename);
}

std::string ConfigDialog::GetFile() const
{
  return file_edit_->text().toStdString();
}

void ConfigDialog::SetFile(const std::string& file)
{
  file_edit_->setText(QString::fromStdString(file));
}

bool ConfigDialog::GetHide() const
{
  return hide_box_->isChecked();
}

void ConfigDialog::SetHide(const bool hide)
{
  hide_box_->setChecked(hide);
}

}

