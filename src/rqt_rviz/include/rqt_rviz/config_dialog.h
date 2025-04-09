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

#ifndef rqt_rviz__ConfigDialog_H
#define rqt_rviz__ConfigDialog_H

#include <QCheckBox>
#include <QDialog>
#include <QLineEdit>

namespace rqt_rviz
{

class ConfigDialog : public QDialog
{

  Q_OBJECT

public:

  /** @brief Constructor. */
  ConfigDialog();

  /** @brief Destructor. */
  ~ConfigDialog();

  /** @brief Populate the file path line edit. */
  void SetFile(const std::string& file);

  /** @brief Get the file path entered by the user. */
  std::string GetFile() const;

  /** @brief Get the hide menu option. */
  bool GetHide() const;

  /** @brief Set the hide menu option. */
  void SetHide(const bool hide);

private slots:

  /** @brief Callback when the browse button is pressed. */
  void OnBrowse();

private:

  /** @brief Holds the file path. */
  QLineEdit* file_edit_;

  /** @brief Holds the boolean for whether to hide the menu. */
  QCheckBox* hide_box_;
};

}

#endif // rqt_rviz__ConfigDialog_H
